class ScoringService:
    @staticmethod
    def calculate_scores(
        traffic_index: float,
        pop_density_index: float,
        renters_share: float,
        income_index: float,
        poi_index: float,
        grid_proxy: float = 0.5
    ):
        """
        Calculates sub-scores and overall score based on heuristic formulas.
        
        score_demand = 0.4 * traffic + 0.3 * pop_density + 0.3 * poi
        score_equity = 0.5 * (1 - income) + 0.5 * renters_share
        score_traffic = traffic_index
        score_grid = grid_proxy
        
        score_overall = 0.45 * demand + 0.35 * equity + 0.20 * grid
        """
        
        # Ensure inputs are clamped 0-1 (just in case)
        traffic_index = max(0, min(1, traffic_index))
        pop_density_index = max(0, min(1, pop_density_index))
        renters_share = max(0, min(1, renters_share))
        income_index = max(0, min(1, income_index))
        poi_index = max(0, min(1, poi_index))
        
        # 1. Demand Score
        score_demand = (0.4 * traffic_index) + (0.3 * pop_density_index) + (0.3 * poi_index)
        
        # 2. Equity Score (Higher score for lower income, higher renter share)
        # Invert income index so 0 (low income) -> 1 (high priority)
        score_equity = (0.5 * (1.0 - income_index)) + (0.5 * renters_share)
        
        # 3. Traffic Score
        score_traffic = traffic_index
        
        # 4. Grid Score (Placeholder)
        score_grid = grid_proxy
        
        # 5. Overall Score
        score_overall = (0.45 * score_demand) + (0.35 * score_equity) + (0.20 * score_grid)
        
        return {
            "score_demand": round(score_demand * 100, 1),
            "score_equity": round(score_equity * 100, 1),
            "score_traffic": round(score_traffic * 100, 1),
            "score_grid": round(score_grid * 100, 1),
            "score_overall": round(score_overall * 100, 1)
        }

    @staticmethod
    def estimate_daily_kwh(traffic_index: float, pop_density_index: float):
        """
        daily_kWh = (base + alpha * traffic + beta * pop) * avg_kWh_per_session
        """
        BASE_SESSIONS = 4.0
        ALPHA = 8.0
        BETA = 6.0
        AVG_KWH = 25.0
        
        expected_sessions = BASE_SESSIONS + (ALPHA * traffic_index) + (BETA * pop_density_index)
        daily_kwh = expected_sessions * AVG_KWH
        
        return round(daily_kwh, 1)
