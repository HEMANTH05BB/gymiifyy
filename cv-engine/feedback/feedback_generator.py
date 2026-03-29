def generate_feedback(metrics):
    joint_feedback = []
    incorrect = []
    scores = []
    suggestions = []

    for item in metrics:
        delta = abs(item["measured"] - item["target"])
        status = "good" if delta <= item["tolerance"] else "adjust"
        suggestion = "Great form" if status == "good" else item["suggestion"]

        joint_feedback.append(
            {
                "joint": item["joint"],
                "measured_angle": round(item["measured"], 2),
                "target_angle": item["target"],
                "delta": round(delta, 2),
                "status": status,
                "suggestion": suggestion,
            }
        )

        scores.append(max(0.0, 100.0 - delta))
        if status == "adjust":
            incorrect.append(item["joint"])
            suggestions.append(suggestion)

    accuracy = round(sum(scores) / max(1, len(scores)), 2)
    overall = "Excellent control and posture." if accuracy >= 90 else " ".join(suggestions) or "Good effort."

    return {
        "accuracy": accuracy,
        "overall": overall,
        "joint_feedback": joint_feedback,
        "incorrect_joints": incorrect,
    }
