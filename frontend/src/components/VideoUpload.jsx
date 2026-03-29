import { useState } from "react";

import { analyzeVideo } from "../services/api";

export default function VideoUpload({ userId, exercise, onSummary }) {
  const [status, setStatus] = useState("Upload MP4 to run frame-by-frame posture analysis.");

  async function handleVideo(event) {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      setStatus("Analyzing video, this may take a moment...");
      const summary = await analyzeVideo({ exercise, userId, file });
      onSummary(summary);
      setStatus("Video analysis complete.");
    } catch {
      setStatus("Video analysis failed. Check MP4 format and backend logs.");
    }
  }

  return (
    <div className="glow-card rounded-2xl p-4">
      <h3 className="text-xl">Video Upload Mode</h3>
      <p className="mt-2 text-sm text-slate-300">{status}</p>
      <label className="mt-3 inline-block rounded-lg border border-dashed border-[#ff8c42] px-4 py-3 text-sm">
        Upload MP4
        <input type="file" accept="video/mp4" onChange={handleVideo} className="hidden" />
      </label>
    </div>
  );
}
