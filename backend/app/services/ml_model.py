from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

from app.core.config import settings


FEATURES: list[str] = [
    "traffic_index",
    "pop_density_index",
    "renters_share",
    "income_index",
    "poi_index",
]


@dataclass(frozen=True)
class LinearModelArtifact:
    features: list[str]
    coef: list[float]
    intercept: float
    trained_on: str
    rmse: float

    def predict_one(self, x: dict[str, float]) -> float:
        vec = np.array([float(x[f]) for f in self.features], dtype=float)
        return float(np.dot(vec, np.array(self.coef, dtype=float)) + float(self.intercept))


def _artifact_path() -> Path:
    # model_path is relative to backend/ by default in docker
    return Path(settings.model_path)


def load_or_train_model(*, force_retrain: bool = False) -> LinearModelArtifact:
    path = _artifact_path()

    if (not force_retrain) and path.exists():
        with path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        return LinearModelArtifact(
            features=list(raw["features"]),
            coef=[float(v) for v in raw["coef"]],
            intercept=float(raw["intercept"]),
            trained_on=str(raw.get("trained_on", "unknown")),
            rmse=float(raw.get("rmse", float("nan"))),
        )

    artifact = train_synthetic_model(write_artifact=True)
    return artifact


def train_synthetic_model(*, n: int = 3000, seed: int = 7, write_artifact: bool = True) -> LinearModelArtifact:
    """Train a small regression model on synthetic data.

    Portfolio note:
    - In v1 we do not have real "kWh dispensed" labels.
    - We simulate plausible feature distributions + a noisy target function.

    The goal is to demonstrate end-to-end ML plumbing, not claim real-world accuracy.
    """

    rng = np.random.default_rng(seed)

    X = np.column_stack(
        [
            rng.beta(2.0, 2.0, size=n),  # traffic_index
            rng.beta(2.2, 2.5, size=n),  # pop_density_index
            rng.beta(2.0, 3.0, size=n),  # renters_share
            rng.beta(2.5, 2.0, size=n),  # income_index
            rng.beta(2.0, 2.2, size=n),  # poi_index
        ]
    )

    # A simple, interpretable generating process (plus noise)
    traffic = X[:, 0]
    pop = X[:, 1]
    renters = X[:, 2]
    income = X[:, 3]
    poi = X[:, 4]

    expected_sessions = 4.0 + 8.0 * traffic + 6.0 * pop + 1.5 * poi
    # Equity effect: slightly higher utilization where renters higher, slightly lower in highest-income areas
    expected_sessions += 1.0 * renters - 0.5 * income

    avg_kwh = 25.0
    y = expected_sessions * avg_kwh

    # Add noise to simulate unobserved factors
    y = y + rng.normal(0.0, 12.0, size=n)

    model = Ridge(alpha=1.0, random_state=seed)
    model.fit(X, y)

    y_pred = model.predict(X)
    rmse = float(np.sqrt(mean_squared_error(y, y_pred)))

    artifact = LinearModelArtifact(
        features=list(FEATURES),
        coef=[float(v) for v in model.coef_.tolist()],
        intercept=float(model.intercept_),
        trained_on="synthetic",
        rmse=rmse,
    )

    if write_artifact:
        path = _artifact_path()
        os.makedirs(path.parent, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(
                {
                    "model_type": "ridge",
                    "features": artifact.features,
                    "coef": artifact.coef,
                    "intercept": artifact.intercept,
                    "trained_on": artifact.trained_on,
                    "rmse": artifact.rmse,
                },
                f,
                indent=2,
            )

    return artifact
