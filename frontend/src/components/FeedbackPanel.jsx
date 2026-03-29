export default function FeedbackPanel({ analysis }) {
  if (!analysis) {
    return (
      <section className="glow-card rounded-2xl p-5 stagger-enter" style={{ animationDelay: "0.1s" }}>
        <p className="text-sm text-slate-300">Start a workout mode to see posture feedback.</p>
      </section>
    );
  }

  return (
    <section className="glow-card rounded-2xl p-5 stagger-enter" style={{ animationDelay: "0.1s" }}>
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-2xl">Live Coaching</h3>
        <span className="rounded-full bg-[#233f52] px-3 py-1 text-sm">
          Accuracy {analysis.posture_accuracy}%
        </span>
      </div>

      <div className="h-3 overflow-hidden rounded-full bg-[#203445]">
        <div
          className="h-full rounded-full bg-[#77f2c7] transition-all duration-300"
          style={{ width: `${analysis.posture_accuracy}%` }}
        />
      </div>

      <p className="mt-3 text-sm text-slate-100">{analysis.overall_feedback}</p>

      <div className="mt-4 grid gap-2">
        {analysis.joint_feedback?.map((item) => (
          <div key={item.joint} className="rounded-lg border border-[#2e4f61] bg-[#0f2534] p-2 text-sm">
            <p className="font-semibold capitalize">{item.joint}</p>
            <p className={item.status === "adjust" ? "text-[#ff8c42]" : "text-[#77f2c7]"}>{item.suggestion}</p>
          </div>
        ))}
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-3 text-sm">
        <span>Rep count: {analysis.rep_count}</span>
        <span>XP +{analysis.xp_awarded}</span>
        <span>Level {analysis.level}</span>
        <span>Streak {analysis.streak} days</span>
      </div>

      <p className="mt-3 text-sm text-[#77f2c7]">
        {analysis.quote} {analysis.emoji}
      </p>
    </section>
  );
}
