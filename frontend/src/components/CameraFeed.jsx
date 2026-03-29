import { useEffect, useRef, useState } from "react";

import { analyzeLiveFrame } from "../services/api";

const EDGES = [
  [11, 13],
  [13, 15],
  [12, 14],
  [14, 16],
  [11, 12],
  [11, 23],
  [12, 24],
  [23, 24],
  [23, 25],
  [25, 27],
  [24, 26],
  [26, 28],
];

export default function CameraFeed({ userId, exercise, onAnalysis }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [running, setRunning] = useState(false);
  const [status, setStatus] = useState("Camera idle");

  useEffect(() => {
    let stream;

    async function init() {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch {
        setStatus("Camera access denied. Please allow webcam permission.");
      }
    }

    init();
    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  useEffect(() => {
    if (!running) return undefined;

    const interval = setInterval(async () => {
      const video = videoRef.current;
      if (!video || video.readyState < 2) return;

      const tempCanvas = document.createElement("canvas");
      tempCanvas.width = video.videoWidth;
      tempCanvas.height = video.videoHeight;
      const ctx = tempCanvas.getContext("2d");
      ctx.drawImage(video, 0, 0, tempCanvas.width, tempCanvas.height);

      try {
        const imageBase64 = tempCanvas.toDataURL("image/jpeg", 0.72);
        const response = await analyzeLiveFrame({
          exercise,
          image_base64: imageBase64,
          user_id: userId,
        });
        onAnalysis(response);
        drawOverlay(response.keypoints || []);
        setStatus("Analyzing live posture...");
      } catch {
        setStatus("Live analysis failed. Check backend connectivity.");
      }
    }, 1500);

    return () => clearInterval(interval);
  }, [running, exercise, userId, onAnalysis]);

  function drawOverlay(keypoints) {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    if (!canvas || !video || keypoints.length === 0) return;

    canvas.width = video.clientWidth;
    canvas.height = video.clientHeight;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = "#77f2c7";
    ctx.lineWidth = 2;

    EDGES.forEach(([a, b]) => {
      const p1 = keypoints[a];
      const p2 = keypoints[b];
      if (!p1 || !p2) return;
      ctx.beginPath();
      ctx.moveTo(p1.x * canvas.width, p1.y * canvas.height);
      ctx.lineTo(p2.x * canvas.width, p2.y * canvas.height);
      ctx.stroke();
    });

    keypoints.forEach((p) => {
      ctx.fillStyle = "#ff8c42";
      ctx.beginPath();
      ctx.arc(p.x * canvas.width, p.y * canvas.height, 3, 0, Math.PI * 2);
      ctx.fill();
    });
  }

  return (
    <div className="glow-card rounded-2xl p-4">
      <div className="mb-3 flex items-center justify-between">
        <h3 className="text-xl">Live Camera Mode</h3>
        <button
          onClick={() => setRunning((prev) => !prev)}
          className="rounded-full bg-[#ff8c42] px-4 py-2 text-sm font-semibold text-[#0b1220]"
        >
          {running ? "Stop" : "Start"}
        </button>
      </div>
      <p className="mb-3 text-sm text-slate-300">{status}</p>
      <div className="relative overflow-hidden rounded-xl border border-[#315163]">
        <video ref={videoRef} autoPlay playsInline className="w-full object-cover" />
        <canvas ref={canvasRef} className="pointer-events-none absolute inset-0 h-full w-full" />
      </div>
    </div>
  );
}
