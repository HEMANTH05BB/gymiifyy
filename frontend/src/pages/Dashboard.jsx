import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import ProgressBar from "../components/ProgressBar";

export default function Dashboard({ progress }) {
  if (!progress) {
    return (
      <section className="glow-card rounded-2xl p-5">
        <p className="text-sm text-slate-300">No progress yet. Complete a workout to populate dashboard stats.</p>
      </section>
    );
  }

  const accuracyData = progress.accuracy_history?.map((item, index) => ({
    name: `${index + 1}`,
    accuracy: item.accuracy,
  }));
  const xpData = progress.xp_history?.map((item, index) => ({
    name: `${index + 1}`,
    xp: item.total_xp,
  }));

  return (
    <section className="grid gap-5 lg:grid-cols-2">
      <div className="glow-card rounded-2xl p-5">
        <h3 className="text-2xl">Accuracy Trend</h3>
        <div className="mt-4 h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={accuracyData}>
              <XAxis dataKey="name" stroke="#b6c4cf" />
              <YAxis stroke="#b6c4cf" domain={[0, 100]} />
              <Tooltip />
              <Line type="monotone" dataKey="accuracy" stroke="#77f2c7" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="glow-card rounded-2xl p-5">
        <h3 className="text-2xl">XP Growth</h3>
        <div className="mt-4 h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={xpData}>
              <XAxis dataKey="name" stroke="#b6c4cf" />
              <YAxis stroke="#b6c4cf" />
              <Tooltip />
              <Line type="monotone" dataKey="xp" stroke="#ff8c42" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="lg:col-span-2">
        <ProgressBar value={progress.total_xp % 100} label={`Level ${progress.level} progress`} />
      </div>
    </section>
  );
}
