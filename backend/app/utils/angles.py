from __future__ import annotations

from math import acos, degrees, sqrt


def calculate_angle(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]) -> float:
    """Returns angle ABC in degrees."""
    ba = (a[0] - b[0], a[1] - b[1])
    bc = (c[0] - b[0], c[1] - b[1])

    mag_ba = sqrt(ba[0] ** 2 + ba[1] ** 2)
    mag_bc = sqrt(bc[0] ** 2 + bc[1] ** 2)
    if mag_ba == 0 or mag_bc == 0:
        return 0.0

    cosine = (ba[0] * bc[0] + ba[1] * bc[1]) / (mag_ba * mag_bc)
    cosine = max(-1.0, min(1.0, cosine))
    return degrees(acos(cosine))
