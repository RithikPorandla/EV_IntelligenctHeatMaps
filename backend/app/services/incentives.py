from __future__ import annotations

import json
from pathlib import Path


def load_incentives() -> dict:
    path = Path("config/incentives.json")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def incentives_note() -> str:
    data = load_incentives()
    programs = data.get("programs", [])
    if not programs:
        return ""
    names = ", ".join([p.get("name", "") for p in programs if p.get("name")])
    return f"Relevant MA programs: {names}. See official sources for details."
