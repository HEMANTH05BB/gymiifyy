import { useEffect, useState } from "react";

import Dashboard from "./pages/Dashboard";
import Home from "./pages/Home";
import Workout from "./pages/Workout";
import { fetchProgress } from "./services/api";

export default function App() {
  const [activePage, setActivePage] = useState("home");
  const [progress, setProgress] = useState(null);
  const userId = "demo-user";

  async function loadProgress() {
    try {
      const data = await fetchProgress(userId);
      setProgress(data);
    } catch {
      // Keep UI functional if backend is unavailable.
    }
  }

  useEffect(() => {
    loadProgress();
  }, []);

  return (
    <main className="mx-auto min-h-screen w-full max-w-7xl px-4 py-6 md:px-8">
      <header className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-4xl">Gymify Arena</h2>
        <nav className="flex gap-2">
          <button onClick={() => setActivePage("home")} className="rounded-full bg-[#203e4d] px-4 py-2 text-sm">
            Home
          </button>
          <button onClick={() => setActivePage("workout")} className="rounded-full bg-[#203e4d] px-4 py-2 text-sm">
            Workout
          </button>
          <button onClick={() => setActivePage("dashboard")} className="rounded-full bg-[#203e4d] px-4 py-2 text-sm">
            Dashboard
          </button>
        </nav>
      </header>

      {activePage === "home" && <Home onGoWorkout={() => setActivePage("workout")} />}
      {activePage === "workout" && <Workout userId={userId} onAnalysisUpdate={loadProgress} />}
      {activePage === "dashboard" && <Dashboard progress={progress} />}
    </main>
  );
}
