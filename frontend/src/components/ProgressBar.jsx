export default function ProgressBar({ value, max = 100, label = "Progress" }) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));

  return (
    <div className="glow-card rounded-2xl p-4">
      <div className="mb-2 flex items-center justify-between">
        <p className="text-sm text-slate-200">{label}</p>
        <p className="text-sm text-[#77f2c7]">{Math.round(pct)}%</p>
      </div>
      <div className="h-3 overflow-hidden rounded-full bg-[#1f3546]">
        <div
          className="h-full rounded-full bg-gradient-to-r from-[#77f2c7] to-[#ff8c42] transition-all duration-300"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
