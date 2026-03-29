export default function ExerciseSelector({ exercise, setExercise, dayFilter, setDayFilter }) {
  return (
    <div className="glow-card rounded-2xl p-4">
      <h3 className="text-xl">Workout Setup</h3>
      <div className="mt-3 grid gap-3 sm:grid-cols-2">
        <label className="text-sm">
          Exercise
          <select
            value={exercise}
            onChange={(e) => setExercise(e.target.value)}
            className="mt-1 w-full rounded-lg border border-[#2a4a5f] bg-[#102737] p-2"
          >
            <option value="squat">Squats</option>
            <option value="pushup">Push-ups</option>
          </select>
        </label>

        <label className="text-sm">
          Filter
          <select
            value={dayFilter}
            onChange={(e) => setDayFilter(e.target.value)}
            className="mt-1 w-full rounded-lg border border-[#2a4a5f] bg-[#102737] p-2"
          >
            <option value="leg_day">Leg day</option>
            <option value="chest_day">Chest day</option>
          </select>
        </label>
      </div>
    </div>
  );
}
