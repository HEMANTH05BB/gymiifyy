export default function ScoreDisplay({ analysis }) {
  if (!analysis) {
    return (
      <div className="glow-card rounded-2xl p-4 text-sm text-slate-300">
        Posture score will appear after first analysis.
      </div>
    );
  }

  return (
    <div className="glow-card rounded-2xl p-4">
      <div className="flex flex-wrap items-center gap-3 text-sm">
        <span className="rounded-full bg-[#203e4d] px-3 py-1">Accuracy: {analysis.posture_accuracy}%</span>
        <span className="rounded-full bg-[#203e4d] px-3 py-1">Reps: {analysis.rep_count}</span>
        <span className="rounded-full bg-[#203e4d] px-3 py-1">XP +{analysis.xp_awarded}</span>
      </div>
      <p className="mt-3 text-slate-100">{analysis.overall_feedback}</p>
      <p className="mt-2 text-[#77f2c7]">
        {analysis.quote} {analysis.emoji}
      </p>
    </div>
  );
}
