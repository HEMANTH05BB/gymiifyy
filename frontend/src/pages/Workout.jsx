import { useCallback, useState } from "react";

import CameraFeed from "../components/CameraFeed";
import ExerciseSelector from "../components/ExerciseSelector";
import ImageUpload from "../components/ImageUpload";
import ProgressBar from "../components/ProgressBar";
import ScoreDisplay from "../components/ScoreDisplay";
import StreakCounter from "../components/StreakCounter";
import VideoUpload from "../components/VideoUpload";

export default function Workout({ userId, onAnalysisUpdate }) {
  const [mode, setMode] = useState("live");
  const [exercise, setExercise] = useState("squat");
  const [dayFilter, setDayFilter] = useState("leg_day");
  const [analysis, setAnalysis] = useState(null);
  const [videoSummary, setVideoSummary] = useState(null);

  const handleAnalysis = useCallback(
    (result) => {
      setAnalysis(result);
      onAnalysisUpdate(result);
    },
    [onAnalysisUpdate]
  );

  return (
    <section className="grid gap-5">
      <ExerciseSelector
        exercise={exercise}
        setExercise={setExercise}
        dayFilter={dayFilter}
        setDayFilter={setDayFilter}
      />

      <div className="grid gap-5 lg:grid-cols-3">
        <div className="space-y-5 lg:col-span-2">
          {mode === "live" && <CameraFeed userId={userId} exercise={exercise} onAnalysis={handleAnalysis} />}
          {mode === "video" && <VideoUpload userId={userId} exercise={exercise} onSummary={setVideoSummary} />}
          {mode === "image" && <ImageUpload userId={userId} exercise={exercise} onAnalysis={handleAnalysis} />}

          <div className="flex gap-2">
            <button onClick={() => setMode("live")} className="rounded-full bg-[#203e4d] px-4 py-2 text-sm">
              Live
            </button>
            <button onClick={() => setMode("video")} className="rounded-full bg-[#203e4d] px-4 py-2 text-sm">
              Video
            </button>
            <button onClick={() => setMode("image")} className="rounded-full bg-[#203e4d] px-4 py-2 text-sm">
              Image
            </button>
          </div>

          {videoSummary && (
            <div className="glow-card rounded-2xl p-4">
              <h3 className="text-xl">Video Summary</h3>
              <p className="mt-2 text-sm">Average accuracy: {videoSummary.avg_accuracy}%</p>
              <p className="text-sm">Total reps: {videoSummary.total_reps}</p>
              <ul className="mt-2 list-disc pl-5 text-sm text-[#ff8c42]">
                {videoSummary.suggestions.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
          )}
        </div>

        <div className="space-y-5">
          <ScoreDisplay analysis={analysis} />
          <ProgressBar value={analysis?.posture_accuracy || 0} label="Posture Quality" />
          <StreakCounter streak={analysis?.streak || 0} level={analysis?.level || 1} totalXp={analysis?.xp_awarded || 0} />
        </div>
      </div>
    </section>
  );
}
