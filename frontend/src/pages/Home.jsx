export default function Home({ onGoWorkout }) {
  return (
    <section className="stagger-enter rounded-2xl border border-[#2f4b5d] bg-gradient-to-r from-[#0f2536] to-[#122436] p-6">
      <p className="text-sm uppercase tracking-[0.2em] text-[#77f2c7]">AI Gamified Fitness Trainer</p>
      <h1 className="mt-2 text-5xl hero-pulse">Train Smarter. Level Up Daily.</h1>
      <p className="mt-4 max-w-2xl text-slate-200">
        Real-time posture analysis for squats and push-ups with XP, streaks, levels, and actionable corrections.
      </p>
      <button
        onClick={onGoWorkout}
        className="mt-6 rounded-full bg-[#77f2c7] px-6 py-3 text-sm font-bold uppercase tracking-wide text-[#021118]"
      >
        Start Workout
      </button>
    </section>
  );
}
