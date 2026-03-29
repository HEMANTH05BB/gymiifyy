import cv2
import mediapipe as mp

from exercises.pushup import analyze_pushup
from exercises.squat import analyze_squat
from feedback.feedback_generator import generate_feedback


try:
    mp_pose = mp.solutions.pose  # type: ignore[attr-defined]
except AttributeError:
    mp_pose = None


class PoseDetectionEngine:
    def __init__(self):
        self.pose = None
        if mp_pose is not None:
            self.pose = mp_pose.Pose(
                static_image_mode=False,
                model_complexity=1,
                enable_segmentation=False,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5,
            )

    def analyze_frame(self, frame, exercise):
        if self.pose is None:
            return {
                "accuracy": 0,
                "overall": "MediaPipe Pose solutions API unavailable in this environment.",
                "joint_feedback": [],
                "incorrect_joints": ["pose_engine"],
                "keypoints": [],
            }

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.pose.process(rgb)

        if not result.pose_landmarks:
            return {
                "accuracy": 0,
                "overall": "Body not detected clearly. Improve lighting.",
                "joint_feedback": [],
                "incorrect_joints": ["full_body"],
                "keypoints": [],
            }

        landmarks = result.pose_landmarks.landmark
        points = {i: (lm.x, lm.y) for i, lm in enumerate(landmarks)}
        keypoints = [
            {"id": i, "x": lm.x, "y": lm.y, "z": lm.z, "visibility": lm.visibility}
            for i, lm in enumerate(landmarks)
        ]

        if exercise == "squat":
            metrics = analyze_squat(points)
        else:
            metrics = analyze_pushup(points)

        feedback = generate_feedback(metrics)
        feedback["keypoints"] = keypoints
        return feedback
