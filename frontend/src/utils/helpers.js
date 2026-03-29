export function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

export function levelProgress(totalXp) {
  const currentLevelXp = totalXp % 100;
  return currentLevelXp;
}

export function modeBadge(mode) {
  if (mode === "live") return "Live Camera";
  if (mode === "video") return "Video Upload";
  return "Image";
}
