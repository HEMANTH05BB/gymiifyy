from __future__ import annotations

import base64
from dataclasses import dataclass

import cv2
import mediapipe as mp
import numpy as np

from app.models import ExerciseType, JointFeedback
from app.utils.angles import calculate_angle


try:
    mp_pose = mp.solutions.pose  # type: ignore[attr-defined]
except AttributeError:
    mp_pose = None


@dataclass
class PoseAnalysisResult:
    posture_accuracy: float
    rep_count: int
    overall_feedback: str
    joint_feedback: list[JointFeedback]
    incorrect_joints: list[str]
    keypoints: list[dict[str, float]]


class PoseEstimatorService:
    def __init__(self) -> None:
        self._pose = None
        if mp_pose is not None:
            self._pose = mp_pose.Pose(
                static_image_mode=False,
                model_complexity=1,
                enable_segmentation=False,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5,
            )
        self._rep_state: dict[tuple[str, str], str] = {}
        self._rep_counter: dict[tuple[str, str], int] = {}

    @staticmethod
    def _decode_base64_image(image_base64: str) -> np.ndarray:
        if "," in image_base64:
            image_base64 = image_base64.split(",", 1)[1]
        raw = base64.b64decode(image_base64)
        np_buffer = np.frombuffer(raw, np.uint8)
        frame = cv2.imdecode(np_buffer, cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError("Invalid image payload")
        return frame

    def analyze_base64_frame(self, image_base64: str, exercise: ExerciseType, user_id: str) -> PoseAnalysisResult:
        frame = self._decode_base64_image(image_base64)
        return self.analyze_frame(frame, exercise, user_id)

    def analyze_frame(self, frame: np.ndarray, exercise: ExerciseType, user_id: str) -> PoseAnalysisResult:
        if self._pose is None:
            return PoseAnalysisResult(
                posture_accuracy=0,
                rep_count=self._get_reps(user_id, exercise.value),
                overall_feedback=(
                    "MediaPipe Pose solutions API is unavailable in the installed version. "
                    "Install a solutions-compatible build or wire cv-engine/tasks-based landmarker."
                ),
                joint_feedback=[],
                incorrect_joints=["pose_engine"],
                keypoints=[],
            )

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self._pose.process(rgb)

        if not results.pose_landmarks:
            return PoseAnalysisResult(
                posture_accuracy=0,
                rep_count=self._get_reps(user_id, exercise.value),
                overall_feedback="Body not detected clearly. Improve lighting or move fully into frame.",
                joint_feedback=[],
                incorrect_joints=["full_body"],
                keypoints=[],
            )

        landmarks = results.pose_landmarks.landmark
        points = {i: (lm.x, lm.y) for i, lm in enumerate(landmarks)}
        keypoints = [{"id": idx, "x": lm.x, "y": lm.y, "z": lm.z, "visibility": lm.visibility} for idx, lm in enumerate(landmarks)]

        if exercise == ExerciseType.squat:
            analysis = self._analyze_squat(points)
        else:
            analysis = self._analyze_pushup(points)

        reps = self._update_reps(user_id, exercise.value, analysis)

        return PoseAnalysisResult(
            posture_accuracy=analysis["accuracy"],
            rep_count=reps,
            overall_feedback=analysis["overall"],
            joint_feedback=analysis["joint_feedback"],
            incorrect_joints=analysis["incorrect_joints"],
            keypoints=keypoints,
        )

    def _analyze_squat(self, points: dict[int, tuple[float, float]]) -> dict[str, object]:
        # Right side landmarks for squat form estimation.
        hip = points[24]
        knee = points[26]
        ankle = points[28]
        shoulder = points[12]

        knee_angle = calculate_angle(hip, knee, ankle)
        hip_angle = calculate_angle(shoulder, hip, knee)

        targets = {
            "knee": 95.0,
            "hip": 90.0,
        }
        tolerance = 25.0

        jf = self._build_joint_feedback("knee", knee_angle, targets["knee"], tolerance, "Push hips back and align knees over toes")
        hf = self._build_joint_feedback("hip", hip_angle, targets["hip"], tolerance, "Lower until thighs are near parallel")

        joint_feedback = [jf, hf]
        return self._finalize_feedback(joint_feedback)

    def _analyze_pushup(self, points: dict[int, tuple[float, float]]) -> dict[str, object]:
        shoulder = points[12]
        elbow = points[14]
        wrist = points[16]
        hip = points[24]

        elbow_angle = calculate_angle(shoulder, elbow, wrist)
        trunk_angle = calculate_angle(shoulder, hip, points[26])

        targets = {
            "elbow": 90.0,
            "trunk": 170.0,
        }
        tolerance = 30.0

        ef = self._build_joint_feedback("elbow", elbow_angle, targets["elbow"], tolerance, "Bend elbows to about 90 degrees")
        tf = self._build_joint_feedback("trunk", trunk_angle, targets["trunk"], tolerance, "Keep your body in a straight line")

        joint_feedback = [ef, tf]
        return self._finalize_feedback(joint_feedback)

    @staticmethod
    def _build_joint_feedback(joint: str, measured: float, target: float, tolerance: float, suggestion: str) -> JointFeedback:
        delta = abs(measured - target)
        status = "good" if delta <= tolerance else "adjust"
        return JointFeedback(
            joint=joint,
            measured_angle=round(measured, 2),
            target_angle=target,
            delta=round(delta, 2),
            status=status,
            suggestion=suggestion if status == "adjust" else "Great form",
        )

    @staticmethod
    def _finalize_feedback(joint_feedback: list[JointFeedback]) -> dict[str, object]:
        scores = []
        incorrect_joints = []
        suggestions = []

        for item in joint_feedback:
            normalized = max(0.0, 100.0 - item.delta)
            scores.append(normalized)
            if item.status == "adjust":
                incorrect_joints.append(item.joint)
                suggestions.append(item.suggestion)

        accuracy = round(sum(scores) / max(1, len(scores)), 2)
        overall = "Excellent control and posture." if accuracy >= 90 else " ".join(suggestions) or "Good effort, keep refining form."

        return {
            "accuracy": accuracy,
            "overall": overall,
            "joint_feedback": joint_feedback,
            "incorrect_joints": incorrect_joints,
        }

    def _update_reps(self, user_id: str, exercise: str, analysis: dict[str, object]) -> int:
        rep_key = (user_id, exercise)
        state = self._rep_state.get(rep_key, "up")
        accuracy = float(analysis["accuracy"])

        # Simple phase-based rep count using quality threshold.
        if state == "up" and accuracy < 70:
            self._rep_state[rep_key] = "down"
        elif state == "down" and accuracy > 85:
            self._rep_state[rep_key] = "up"
            self._rep_counter[rep_key] = self._rep_counter.get(rep_key, 0) + 1

        return self._rep_counter.get(rep_key, 0)

    def _get_reps(self, user_id: str, exercise: str) -> int:
        return self._rep_counter.get((user_id, exercise), 0)


pose_estimator_service = PoseEstimatorService()
