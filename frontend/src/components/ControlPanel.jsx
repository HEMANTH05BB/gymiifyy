export default function ControlPanel({
  mode,
  setMode,
  exercise,
  setExercise,
  dayFilter,
  setDayFilter,
}) {
  const modes = [
    { id: "live", label: "Live Camera" },
    { id: "video", label: "Video Upload" },
    { id: "image", label: "Image" },
  ];

  return (
    <section className="glow-card rounded-2xl p-4 md:p-6 stagger-enter" style={{ animationDelay: "0.05s" }}>
      <div className="flex flex-wrap gap-2">
        {modes.map((item) => (
          <button
            key={item.id}
            onClick={() => setMode(item.id)}
            className={`rounded-full px-4 py-2 text-sm font-medium transition ${
              mode === item.id ? "bg-[#77f2c7] text-[#001419]" : "bg-[#1b3040] text-white hover:bg-[#233f52]"
            }`}
          >
            {item.label}
          </button>
        ))}
      </div>

      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        <label className="text-sm">
          Exercise
          <select
            className="mt-1 w-full rounded-lg border border-[#2a4a5f] bg-[#102737] p-2"
            value={exercise}
            onChange={(e) => setExercise(e.target.value)}
          >
            <option value="squat">Squats</option>
            <option value="pushup">Push-ups</option>
          </select>
        </label>

        <label className="text-sm">
          Day Filter
          <select
            className="mt-1 w-full rounded-lg border border-[#2a4a5f] bg-[#102737] p-2"
            value={dayFilter}
            onChange={(e) => setDayFilter(e.target.value)}
          >
            <option value="leg_day">Leg day</option>
            <option value="chest_day">Chest day</option>
          </select>
        </label>
      </div>
    </section>
  );
}
