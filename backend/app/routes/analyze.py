from __future__ import annotations

from datetime import datetime
from tempfile import NamedTemporaryFile

import cv2
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.db import database_client
from app.models import AnalysisResponse, DayFilter, ExerciseType, ImageRequest, SessionRecord, VideoAnalysisSummary
from app.services.gamification import gamification_service
from app.services.pose_estimator import pose_estimator_service

router = APIRouter(prefix="/api/analyze", tags=["analysis"])


def _day_filter_from_exercise(exercise: str) -> DayFilter:
    return DayFilter.leg_day if exercise == "squat" else DayFilter.chest_day


@router.post("/image", response_model=AnalysisResponse)
async def analyze_image(request: ImageRequest) -> AnalysisResponse:
    try:
        result = pose_estimator_service.analyze_base64_frame(request.image_base64, request.exercise, request.user_id)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to process image: {exc}") from exc

    xp_awarded, user, quote, emoji = gamification_service.apply_posture_result(
        request.user_id,
        result.posture_accuracy,
        result.rep_count,
    )

    record = SessionRecord(
        user_id=request.user_id,
        exercise=request.exercise,
        day_filter=_day_filter_from_exercise(request.exercise.value),
        accuracy=result.posture_accuracy,
        reps=result.rep_count,
        xp_awarded=xp_awarded,
    )
    await database_client.add_session({**record.model_dump(), "created_at": datetime.utcnow().isoformat()})

    return AnalysisResponse(
        exercise=request.exercise,
        posture_accuracy=result.posture_accuracy,
        rep_count=result.rep_count,
        overall_feedback=result.overall_feedback,
        joint_feedback=result.joint_feedback,
        incorrect_joints=result.incorrect_joints,
        keypoints=result.keypoints,
        xp_awarded=xp_awarded,
        level=user.level,
        streak=user.streak,
        quote=quote,
        emoji=emoji,
    )


@router.post("/live-frame", response_model=AnalysisResponse)
async def analyze_live_frame(request: ImageRequest) -> AnalysisResponse:
    return await analyze_image(request)


@router.post("/video-upload", response_model=VideoAnalysisSummary)
async def analyze_video_upload(
    exercise: str,
    user_id: str,
    file: UploadFile = File(...),
) -> VideoAnalysisSummary:
    try:
        parsed_exercise = ExerciseType(exercise)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="exercise must be 'squat' or 'pushup'") from exc

    if not file.filename.lower().endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Only MP4 files are supported")

    with NamedTemporaryFile(delete=True, suffix=".mp4") as temp:
        temp.write(await file.read())
        temp.flush()

        cap = cv2.VideoCapture(temp.name)
        if not cap.isOpened():
            raise HTTPException(status_code=400, detail="Unable to read uploaded video")

        frame_index = 0
        samples = []
        total_reps = 0
        suggestions = set()

        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frame_index += 1

            if frame_index % 5 != 0:
                continue

            result = pose_estimator_service.analyze_frame(frame, exercise=parsed_exercise, user_id=user_id)
            samples.append(result.posture_accuracy)
            total_reps = max(total_reps, result.rep_count)
            for jf in result.joint_feedback:
                if jf.status == "adjust":
                    suggestions.add(jf.suggestion)

        cap.release()

    if not samples:
        raise HTTPException(status_code=400, detail="No analyzable frames found in video")

    avg_accuracy = round(sum(samples) / len(samples), 2)
    return VideoAnalysisSummary(
        avg_accuracy=avg_accuracy,
        total_reps=total_reps,
        suggestions=sorted(suggestions),
    )
