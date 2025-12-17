"""
Scoring service for computing EV charging site opportunity scores.

This module implements the heuristic scoring logic that evaluates
potential EV charging locations across multiple dimensions:
- Demand: Based on traffic, population density, and points of interest
- Equity: Focuses on lower-income areas and renters
- Traffic: Direct traffic volume indicator
- Grid: Infrastructure readiness (simplified for v1)
- Overall: Weighted combination of all factors
"""
from typing import Dict


class ScoringService:
    """
    Service for computing multi-dimensional site scores.
    
    All feature indexes should be normalized to 0-1 range.
    Output scores are scaled to 0-100 for readability.
    """
    
    # Weights for demand score calculation
    DEMAND_TRAFFIC_WEIGHT = 0.4
    DEMAND_POP_WEIGHT = 0.3
    DEMAND_POI_WEIGHT = 0.3
    
    # Weights for equity score calculation
    EQUITY_INCOME_WEIGHT = 0.5
    EQUITY_RENTERS_WEIGHT = 0.5
    
    # Weights for overall score calculation
    OVERALL_DEMAND_WEIGHT = 0.45
    OVERALL_EQUITY_WEIGHT = 0.35
    OVERALL_GRID_WEIGHT = 0.20
    
    # Daily kWh estimation parameters
    BASE_SESSIONS = 4.0
    TRAFFIC_MULTIPLIER = 8.0
    POP_MULTIPLIER = 6.0
    AVG_KWH_PER_SESSION = 25.0
    
    @classmethod
    def compute_demand_score(
        cls,
        traffic_index: float,
        pop_density_index: float,
        poi_index: float
    ) -> float:
        """
        Compute demand score based on traffic, population, and POI density.
        
        Higher demand indicates more potential charging sessions.
        
        Args:
            traffic_index: Traffic volume index (0-1)
            pop_density_index: Population density index (0-1)
            poi_index: Points of interest density index (0-1)
        
        Returns:
            Demand score (0-100)
        """
        score = (
            cls.DEMAND_TRAFFIC_WEIGHT * traffic_index +
            cls.DEMAND_POP_WEIGHT * pop_density_index +
            cls.DEMAND_POI_WEIGHT * poi_index
        )
        return score * 100.0
    
    @classmethod
    def compute_equity_score(
        cls,
        income_index: float,
        renters_share: float
    ) -> float:
        """
        Compute equity score to prioritize underserved communities.
        
        Higher equity scores favor lower-income areas and renters who
        may not have home charging access.
        
        Args:
            income_index: Income level index (0-1, where 1 = highest income)
            renters_share: Fraction of renters (0-1)
        
        Returns:
            Equity score (0-100)
        """
        # Invert income index - we want to favor lower-income areas
        score = (
            cls.EQUITY_INCOME_WEIGHT * (1.0 - income_index) +
            cls.EQUITY_RENTERS_WEIGHT * renters_share
        )
        return score * 100.0
    
    @classmethod
    def compute_traffic_score(cls, traffic_index: float) -> float:
        """
        Compute traffic score (direct mapping from traffic index).
        
        Args:
            traffic_index: Traffic volume index (0-1)
        
        Returns:
            Traffic score (0-100)
        """
        return traffic_index * 100.0
    
    @classmethod
    def compute_grid_score(
        cls,
        parking_lot_flag: int = 0,
        municipal_parcel_flag: int = 0
    ) -> float:
        """
        Compute grid/infrastructure readiness score.
        
        For v1, this is a simplified placeholder that gives bonus points
        for parking lots and municipal parcels.
        
        Future enhancements could include:
        - Proximity to electrical infrastructure
        - Commercial zoning
        - Existing parking infrastructure
        
        Args:
            parking_lot_flag: 1 if site has parking lot, 0 otherwise
            municipal_parcel_flag: 1 if municipal property, 0 otherwise
        
        Returns:
            Grid score (0-100)
        """
        base_score = 50.0  # Baseline assumption
        if parking_lot_flag:
            base_score += 25.0
        if municipal_parcel_flag:
            base_score += 15.0
        return min(base_score, 100.0)
    
    @classmethod
    def compute_overall_score(
        cls,
        score_demand: float,
        score_equity: float,
        score_grid: float
    ) -> float:
        """
        Compute overall opportunity score as weighted combination.
        
        Args:
            score_demand: Demand score (0-100)
            score_equity: Equity score (0-100)
            score_grid: Grid score (0-100)
        
        Returns:
            Overall score (0-100)
        """
        score = (
            cls.OVERALL_DEMAND_WEIGHT * score_demand +
            cls.OVERALL_EQUITY_WEIGHT * score_equity +
            cls.OVERALL_GRID_WEIGHT * score_grid
        )
        return score
    
    @classmethod
    def estimate_daily_kwh(
        cls,
        traffic_index: float,
        pop_density_index: float
    ) -> float:
        """
        Estimate expected daily charging demand in kWh.
        
        This is a simplified model:
        1. Estimate sessions per day based on traffic and population
        2. Multiply by average kWh per session
        
        Args:
            traffic_index: Traffic volume index (0-1)
            pop_density_index: Population density index (0-1)
        
        Returns:
            Estimated daily kWh demand
        """
        sessions_per_day = (
            cls.BASE_SESSIONS +
            cls.TRAFFIC_MULTIPLIER * traffic_index +
            cls.POP_MULTIPLIER * pop_density_index
        )
        return sessions_per_day * cls.AVG_KWH_PER_SESSION
    
    @classmethod
    def compute_all_scores(cls, features: Dict[str, float]) -> Dict[str, float]:
        """
        Compute all scores and estimates for a site.
        
        Args:
            features: Dictionary with feature indexes:
                - traffic_index
                - pop_density_index
                - renters_share
                - income_index
                - poi_index
                - parking_lot_flag (optional)
                - municipal_parcel_flag (optional)
        
        Returns:
            Dictionary with all scores and estimates
        """
        # Extract features with defaults
        traffic_index = features.get('traffic_index', 0.0)
        pop_density_index = features.get('pop_density_index', 0.0)
        renters_share = features.get('renters_share', 0.0)
        income_index = features.get('income_index', 0.0)
        poi_index = features.get('poi_index', 0.0)
        parking_lot_flag = features.get('parking_lot_flag', 0)
        municipal_parcel_flag = features.get('municipal_parcel_flag', 0)
        
        # Compute individual scores
        score_demand = cls.compute_demand_score(
            traffic_index, pop_density_index, poi_index
        )
        score_equity = cls.compute_equity_score(income_index, renters_share)
        score_traffic = cls.compute_traffic_score(traffic_index)
        score_grid = cls.compute_grid_score(
            parking_lot_flag, municipal_parcel_flag
        )
        score_overall = cls.compute_overall_score(
            score_demand, score_equity, score_grid
        )
        
        # Estimate daily kWh
        daily_kwh_estimate = cls.estimate_daily_kwh(
            traffic_index, pop_density_index
        )
        
        return {
            'score_demand': score_demand,
            'score_equity': score_equity,
            'score_traffic': score_traffic,
            'score_grid': score_grid,
            'score_overall': score_overall,
            'daily_kwh_estimate': daily_kwh_estimate,
        }
