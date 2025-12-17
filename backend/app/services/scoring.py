from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScoringConfig:
    """Heuristic scoring configuration.

    All indices are expected in [0, 1]. Scores are returned in [0, 100].
    """

    demand_w_traffic: float = 0.4
    demand_w_pop: float = 0.3
    demand_w_poi: float = 0.3

    equity_w_low_income: float = 0.5
    equity_w_renters: float = 0.5

    overall_w_demand: float = 0.45
    overall_w_equity: float = 0.35
    overall_w_grid: float = 0.20

    # Daily kWh estimate
    base_sessions: float = 4.0
    alpha_sessions_traffic: float = 8.0
    beta_sessions_pop: float = 6.0
    avg_kwh_per_session: float = 25.0


DEFAULT_SCORING = ScoringConfig()


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def score_demand(*, traffic_index: float, pop_density_index: float, poi_index: float, cfg: ScoringConfig = DEFAULT_SCORING) -> float:
    t = _clamp01(traffic_index)
    p = _clamp01(pop_density_index)
    poi = _clamp01(poi_index)
    s01 = cfg.demand_w_traffic * t + cfg.demand_w_pop * p + cfg.demand_w_poi * poi
    return 100.0 * _clamp01(s01)


def score_equity(*, renters_share: float, income_index: float, cfg: ScoringConfig = DEFAULT_SCORING) -> float:
    r = _clamp01(renters_share)
    inc = _clamp01(income_index)
    low_income = 1.0 - inc
    s01 = cfg.equity_w_low_income * low_income + cfg.equity_w_renters * r
    return 100.0 * _clamp01(s01)


def score_grid_placeholder(*, traffic_index: float) -> float:
    """Placeholder grid score.

    In v1 we keep this simple and transparent: grid score ~= road proximity.
    With real GIS layers later, this can be replaced by zoning/land-use/parking.
    """

    return 100.0 * _clamp01(traffic_index)


def daily_kwh_estimate(*, traffic_index: float, pop_density_index: float, cfg: ScoringConfig = DEFAULT_SCORING) -> float:
    t = _clamp01(traffic_index)
    p = _clamp01(pop_density_index)
    sessions = cfg.base_sessions + cfg.alpha_sessions_traffic * t + cfg.beta_sessions_pop * p
    return float(sessions * cfg.avg_kwh_per_session)


def compute_all_scores(
    *,
    traffic_index: float,
    pop_density_index: float,
    renters_share: float,
    income_index: float,
    poi_index: float,
    cfg: ScoringConfig = DEFAULT_SCORING,
) -> dict[str, float]:
    sd = score_demand(traffic_index=traffic_index, pop_density_index=pop_density_index, poi_index=poi_index, cfg=cfg)
    se = score_equity(renters_share=renters_share, income_index=income_index, cfg=cfg)
    st = 100.0 * _clamp01(traffic_index)
    sg = score_grid_placeholder(traffic_index=traffic_index)

    overall01 = cfg.overall_w_demand * (sd / 100.0) + cfg.overall_w_equity * (se / 100.0) + cfg.overall_w_grid * (sg / 100.0)
    so = 100.0 * _clamp01(overall01)

    kwh = daily_kwh_estimate(traffic_index=traffic_index, pop_density_index=pop_density_index, cfg=cfg)

    return {
        "score_demand": sd,
        "score_equity": se,
        "score_traffic": st,
        "score_grid": sg,
        "score_overall": so,
        "daily_kwh_estimate": kwh,
    }
