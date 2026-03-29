# AI Gamified Fitness Trainer

Full-stack gym coaching app with computer-vision posture analysis, real-time feedback, and gamification (XP, levels, streaks).

## Stack

- Frontend: React + Tailwind CSS + Recharts
- Backend API: FastAPI
- Computer Vision: OpenCV + MediaPipe Pose
- Database: MongoDB (optional; in-memory fallback enabled)

## Project Structure

```
ai-fitness-trainer/
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       ├── utils/
│       └── App.jsx
├── backend/
│   ├── app/                  # Core FastAPI implementation
│   ├── controllers/          # Compatibility wrappers
│   ├── routes/               # Compatibility wrappers
│   ├── services/             # Compatibility wrappers
│   ├── models/               # Compatibility wrappers
│   ├── config/               # Compatibility wrappers
│   └── server.py
├── cv-engine/
│   ├── main.py
│   ├── pose_detection.py
│   ├── angle_calculator.py
│   ├── exercises/
│   │   ├── squat.py
│   │   └── pushup.py
│   ├── feedback/
│   │   └── feedback_generator.py
│   └── utils/
├── database/
│   └── schema.md
├── uploads/
├── package.json
└── README.md
```

## Implemented Features

### 1) Input Modes

- Live Camera Mode:
	- Captures webcam frames in browser
	- Sends frames to `/api/analyze/live-frame`
	- Displays real-time posture score, rep count, and feedback
	- Draws pose skeleton overlay from returned keypoints
- Video Upload Mode:
	- Accepts MP4 upload
	- Processes sampled frames server-side
	- Returns average accuracy, total reps, correction suggestions
- Image Mode:
	- Upload single image
	- Returns posture analysis and coaching suggestions

### 2) Exercise Support

- Squats:
	- Knee and hip angle checks against target posture
- Push-ups:
	- Elbow and trunk angle checks against target posture

### 3) Posture Analysis

- MediaPipe Pose keypoint extraction
- Joint-angle computation
- Accuracy score generation
- Body-part-wise error detection
- Correction hints when joints are outside tolerance

### 4) Gamification

- XP logic:
	- +10 XP when posture is >= 80%
	- +20 XP when posture is >= 95%
	- Small additional XP from reps
- Leveling:
	- Level increases every 100 XP
- Streak:
	- Daily workout streak increments for consecutive days
	- Resets when a day is missed
- Motivational quotes and emojis

### 5) Dashboard

- Accuracy trend chart
- XP growth chart
- Level progress bar
- Streak and level indicators

## API Endpoints

- `POST /api/analyze/live-frame`
- `POST /api/analyze/image`
- `POST /api/analyze/video-upload?exercise=squat|pushup&user_id=...`
- `GET /api/progress/{user_id}`
- `GET /health`

## Run Instructions

## 1. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173` and calls backend `http://localhost:8000`.

To override API URL, set `VITE_API_BASE_URL` in frontend env.

## Step-by-Step Implementation Plan

1. Start with squat + push-up static image analysis (`/api/analyze/image`).
2. Add live camera frame streaming and overlay feedback.
3. Add MP4 frame sampling and video summary endpoint.
4. Expand gamification persistence to MongoDB users collection.
5. Add WebSocket live feedback for lower latency.
6. Add more exercises (lunges, planks, deadlifts) via `cv-engine/exercises/` modules.
7. Add voice feedback + coach personality modes.
8. Add mobile app and wearable integration.

## Notes

- For low-light robustness, improve camera lighting and use higher detection confidence tuning.
- Real-time performance can be improved by reducing frame size and inference frequency.
