import { useState } from "react";

import { analyzeImage } from "../services/api";
import { fileToBase64 } from "../utils/helpers";

export default function ImageUpload({ userId, exercise, onAnalysis }) {
  const [status, setStatus] = useState("Upload a photo to analyze posture.");

  async function handleFile(event) {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      setStatus("Processing image...");
      const base64 = await fileToBase64(file);
      const result = await analyzeImage({
        exercise,
        image_base64: base64,
        user_id: userId,
      });
      onAnalysis(result);
      setStatus("Image analysis completed.");
    } catch {
      setStatus("Image analysis failed. Ensure backend is running.");
    }
  }

  return (
    <div className="glow-card rounded-2xl p-4">
      <h3 className="text-xl">Image Mode</h3>
      <p className="mt-2 text-sm text-slate-300">{status}</p>
      <label className="mt-3 inline-block rounded-lg border border-dashed border-[#77f2c7] px-4 py-3 text-sm">
        Upload JPG/PNG
        <input type="file" accept="image/*" onChange={handleFile} className="hidden" />
      </label>
    </div>
  );
}
