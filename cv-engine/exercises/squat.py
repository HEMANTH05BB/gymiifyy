from angle_calculator import calculate_angle


def analyze_squat(points):
    hip = points[24]
    knee = points[26]
    ankle = points[28]
    shoulder = points[12]

    knee_angle = calculate_angle(hip, knee, ankle)
    hip_angle = calculate_angle(shoulder, hip, knee)

    targets = {"knee": 95.0, "hip": 90.0}
    tolerance = 25.0

    metrics = [
        {
            "joint": "knee",
            "measured": knee_angle,
            "target": targets["knee"],
            "suggestion": "Push hips back and align knees over toes",
            "tolerance": tolerance,
        },
        {
            "joint": "hip",
            "measured": hip_angle,
            "target": targets["hip"],
            "suggestion": "Lower until thighs are near parallel",
            "tolerance": tolerance,
        },
    ]

    return metrics
