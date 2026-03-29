export default function StreakCounter({ streak = 0, level = 1, totalXp = 0 }) {
  return (
    <div className="glow-card rounded-2xl p-4">
      <h3 className="text-xl">Gamification</h3>
      <div className="mt-3 flex gap-3 text-sm">
        <span className="rounded-full bg-[#233f52] px-3 py-1">Streak: {streak} days</span>
        <span className="rounded-full bg-[#233f52] px-3 py-1">Level: {level}</span>
        <span className="rounded-full bg-[#233f52] px-3 py-1">Total XP: {totalXp}</span>
      </div>
    </div>
  );
}
