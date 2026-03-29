from __future__ import annotations

from datetime import date, datetime, timedelta

from app.models import UserProgress


MOTIVATIONAL_QUOTES = [
    ("Strong form, stronger you.", "💪"),
    ("Consistency beats intensity over time.", "🔥"),
    ("One rep at a time, one level at a time.", "🏆"),
    ("You are building discipline, not just muscles.", "🚀"),
]


class GamificationService:
    def __init__(self) -> None:
        self._users: dict[str, UserProgress] = {}

    def get_or_create_user(self, user_id: str) -> UserProgress:
        if user_id not in self._users:
            self._users[user_id] = UserProgress(user_id=user_id)
        return self._users[user_id]

    def apply_posture_result(self, user_id: str, accuracy: float, reps: int) -> tuple[int, UserProgress, str, str]:
        user = self.get_or_create_user(user_id)

        xp_awarded = 0
        if accuracy >= 80:
            xp_awarded += 10
        if accuracy >= 95:
            xp_awarded += 20

        # Small reward for volume without overpowering posture quality.
        xp_awarded += min(20, reps * 2)

        user.total_xp += xp_awarded
        user.level = max(1, (user.total_xp // 100) + 1)

        today = date.today()
        if user.last_workout_date is None:
            user.streak = 1
        else:
            last = datetime.strptime(user.last_workout_date, "%Y-%m-%d").date()
            if today == last:
                user.streak = max(1, user.streak)
            elif today - last == timedelta(days=1):
                user.streak += 1
            else:
                user.streak = 1

        user.last_workout_date = today.isoformat()
        user.xp_history.append({"date": today.isoformat(), "xp": xp_awarded, "total_xp": user.total_xp})
        user.accuracy_history.append({"date": today.isoformat(), "accuracy": round(accuracy, 2)})

        quote, emoji = MOTIVATIONAL_QUOTES[user.total_xp % len(MOTIVATIONAL_QUOTES)]
        return xp_awarded, user, quote, emoji

    def get_progress(self, user_id: str) -> UserProgress:
        return self.get_or_create_user(user_id)


gamification_service = GamificationService()
