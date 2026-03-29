from angle_calculator import calculate_angle


def analyze_pushup(points):
    shoulder = points[12]
    elbow = points[14]
    wrist = points[16]
    hip = points[24]
    knee = points[26]

    elbow_angle = calculate_angle(shoulder, elbow, wrist)
    trunk_angle = calculate_angle(shoulder, hip, knee)

    targets = {"elbow": 90.0, "trunk": 170.0}
    tolerance = 30.0

    metrics = [
        {
            "joint": "elbow",
            "measured": elbow_angle,
            "target": targets["elbow"],
            "suggestion": "Bend elbows to about 90 degrees",
            "tolerance": tolerance,
        },
        {
            "joint": "trunk",
            "measured": trunk_angle,
            "target": targets["trunk"],
            "suggestion": "Keep your body in a straight line",
            "tolerance": tolerance,
        },
    ]

    return metrics
