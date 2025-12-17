from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = REPO_ROOT / "data" / "raw"
PROCESSED_DIR = REPO_ROOT / "data" / "processed"


@dataclass(frozen=True)
class WorcesterBBox:
    west: float = -71.93
    south: float = 42.20
    east: float = -71.71
    north: float = 42.34


WORCESTER_BBOX = WorcesterBBox()


def ensure_dirs() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
