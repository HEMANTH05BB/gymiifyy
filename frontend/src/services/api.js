import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
  timeout: 30000,
});

export async function analyzeLiveFrame(payload) {
  const { data } = await api.post("/api/analyze/live-frame", payload);
  return data;
}

export async function analyzeImage(payload) {
  const { data } = await api.post("/api/analyze/image", payload);
  return data;
}

export async function analyzeVideo({ exercise, userId, file }) {
  const formData = new FormData();
  formData.append("file", file);

  const { data } = await api.post(`/api/analyze/video-upload?exercise=${exercise}&user_id=${userId}`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return data;
}

export async function fetchProgress(userId) {
  const { data } = await api.get(`/api/progress/${userId}`);
  return data;
}
