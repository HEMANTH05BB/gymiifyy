from __future__ import annotations

from fastapi import APIRouter

from app.db import database_client
from app.services.gamification import gamification_service

router = APIRouter(prefix="/api/progress", tags=["progress"])


@router.get("/{user_id}")
async def get_progress(user_id: str) -> dict:
    progress = gamification_service.get_progress(user_id)
    sessions = await database_client.get_sessions_by_user(user_id)

    return {
        "user_id": progress.user_id,
        "total_xp": progress.total_xp,
        "level": progress.level,
        "streak": progress.streak,
        "last_workout_date": progress.last_workout_date,
        "xp_history": progress.xp_history,
        "accuracy_history": progress.accuracy_history,
        "sessions": sessions,
    }
