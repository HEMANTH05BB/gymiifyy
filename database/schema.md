# Database Schema (MongoDB)

## users

```json
{
  "_id": "ObjectId",
  "user_id": "string",
  "total_xp": "number",
  "level": "number",
  "streak": "number",
  "last_workout_date": "YYYY-MM-DD",
  "xp_history": [
    { "date": "YYYY-MM-DD", "xp": "number", "total_xp": "number" }
  ],
  "accuracy_history": [
    { "date": "YYYY-MM-DD", "accuracy": "number" }
  ]
}
```

## sessions

```json
{
  "_id": "ObjectId",
  "user_id": "string",
  "exercise": "squat|pushup",
  "day_filter": "leg_day|chest_day",
  "accuracy": "number",
  "reps": "number",
  "xp_awarded": "number",
  "created_at": "ISO Date"
}
```

## indexes

- `users.user_id` unique
- `sessions.user_id` ascending
- `sessions.created_at` ascending
