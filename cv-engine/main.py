import argparse

import cv2

from pose_detection import PoseDetectionEngine


def run_image(engine, image_path, exercise):
    frame = cv2.imread(image_path)
    if frame is None:
        raise ValueError("Unable to read image")
    result = engine.analyze_frame(frame, exercise)
    print(result)


def run_video(engine, video_path, exercise):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Unable to open video")

    samples = []
    frame_index = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        frame_index += 1
        if frame_index % 5 != 0:
            continue

        samples.append(engine.analyze_frame(frame, exercise)["accuracy"])

    cap.release()
    if not samples:
        print({"avg_accuracy": 0})
        return

    print({"avg_accuracy": round(sum(samples) / len(samples), 2), "samples": len(samples)})


def main():
    parser = argparse.ArgumentParser(description="AI fitness posture detection")
    parser.add_argument("--mode", choices=["image", "video"], required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--exercise", choices=["squat", "pushup"], required=True)
    args = parser.parse_args()

    engine = PoseDetectionEngine()

    if args.mode == "image":
        run_image(engine, args.input, args.exercise)
    else:
        run_video(engine, args.input, args.exercise)


if __name__ == "__main__":
    main()
