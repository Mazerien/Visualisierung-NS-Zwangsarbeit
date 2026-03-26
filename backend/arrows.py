from dataclasses import dataclass
from typing import List

TARGET_CITY = "Schwenningen"
TARGET_COUNTRY = "Deutschland"

@dataclass
class Arrow:
    start_city: str
    start_country: str
    color: str
    width: float = 3.0         # Line thickness
    dash: list[int] | None = None  # Dash pattern, e.g., [5, 5]
    opacity: float = 0.8       # Transparency (0.0-1.0)

DEFAULT_ARROWS: List[Arrow] = [
    Arrow("Berlin", "Deutschland", color="red", width=10.5, dash=None, opacity=1.0),
    Arrow("Paris", "France", color="blue", width=20.5, dash=None, opacity=0.3),
]

SECOND_ARROW_SET: List[Arrow] = [
    Arrow("Warsaw", "Poland", color="black", width=4.0, dash=None, opacity=1.0),
    Arrow("Vienna", "Austria", color="yellow", width=3.0, dash=[2, 2], opacity=0.6),
]

def expand_arrows(arrows: List[Arrow], target=(TARGET_CITY, TARGET_COUNTRY)):
    """
    Convert simplified Arrow objects into full tuples for geo_map.py:
    (start_city, start_country, target_city, target_country, color, width, dash, opacity)
    """
    target_city, target_country = target
    return [
        (
            arrow.start_city,
            arrow.start_country,
            target_city,
            target_country,
            arrow.color,
            arrow.width,
            arrow.dash,
            arrow.opacity
        )
        for arrow in arrows
    ]

def get_arrows(set_name: str = "default"):
    """
    Return the expanded arrow set for the given name.
    """
    match set_name:
        case "2":
            arrows = SECOND_ARROW_SET
        case "default":
            arrows = DEFAULT_ARROWS
        case _:
            arrows = DEFAULT_ARROWS

    return expand_arrows(arrows)