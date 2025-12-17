from __future__ import annotations

from app.services.scoring import compute_all_scores


def test_compute_all_scores_ranges() -> None:
    scores = compute_all_scores(
        traffic_index=0.7,
        pop_density_index=0.6,
        renters_share=0.4,
        income_index=0.5,
        poi_index=0.8,
    )

    for k in ["score_demand", "score_equity", "score_traffic", "score_grid", "score_overall"]:
        assert 0.0 <= scores[k] <= 100.0

    assert scores["daily_kwh_estimate"] > 0
