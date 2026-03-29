from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ExerciseType(str, Enum):
    squat = "squat"
    pushup = "pushup"


class DayFilter(str, Enum):
    leg_day = "leg_day"
    chest_day = "chest_day"


class JointFeedback(BaseModel):
    joint: str
    measured_angle: float
    target_angle: float
    delta: float
    status: str
    suggestion: str


class AnalysisResponse(BaseModel):
    exercise: ExerciseType
    posture_accuracy: float = Field(ge=0, le=100)
    rep_count: int = 0
    overall_feedback: str
    joint_feedback: list[JointFeedback]
    incorrect_joints: list[str]
    keypoints: list[dict[str, float | int]] = Field(default_factory=list)
    xp_awarded: int
    level: int
    streak: int
    quote: str
    emoji: str


class LiveFrameRequest(BaseModel):
    exercise: ExerciseType
    image_base64: str
    user_id: str = "demo-user"


class ImageRequest(BaseModel):
    exercise: ExerciseType
    image_base64: str
    user_id: str = "demo-user"


class VideoAnalysisSummary(BaseModel):
    avg_accuracy: float = Field(ge=0, le=100)
    total_reps: int
    suggestions: list[str]


class SessionRecord(BaseModel):
    user_id: str
    exercise: ExerciseType
    day_filter: DayFilter
    accuracy: float
    reps: int
    xp_awarded: int
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserProgress(BaseModel):
    user_id: str
    total_xp: int = 0
    level: int = 1
    streak: int = 0
    last_workout_date: str | None = None
    xp_history: list[dict[str, Any]] = Field(default_factory=list)
    accuracy_history: list[dict[str, Any]] = Field(default_factory=list)
