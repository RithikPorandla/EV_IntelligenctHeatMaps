from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class City:
    slug: str
    name: str
    # WGS84 bbox
    west: float
    south: float
    east: float
    north: float


SUPPORTED_CITIES: list[City] = [
    City(
        slug="worcester",
        name="Worcester, MA",
        # Approx Worcester bbox (WGS84)
        west=-71.93,
        south=42.20,
        east=-71.71,
        north=42.34,
    ),
]


def get_city(slug: str) -> City | None:
    for c in SUPPORTED_CITIES:
        if c.slug == slug:
            return c
    return None
