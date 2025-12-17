"""
Tests for scoring service.
"""
import pytest
from app.services.scoring import ScoringService


class TestScoringService:
    """Test suite for ScoringService."""
    
    def test_demand_score_calculation(self):
        """Test demand score computation."""
        score = ScoringService.compute_demand_score(
            traffic_index=0.8,
            pop_density_index=0.6,
            poi_index=0.7
        )
        
        # Expected: 0.4*0.8 + 0.3*0.6 + 0.3*0.7 = 0.71 * 100 = 71.0
        assert score == pytest.approx(71.0, rel=0.01)
    
    def test_equity_score_calculation(self):
        """Test equity score computation."""
        score = ScoringService.compute_equity_score(
            income_index=0.3,  # Lower income area
            renters_share=0.6   # 60% renters
        )
        
        # Expected: 0.5*(1-0.3) + 0.5*0.6 = 0.5*0.7 + 0.3 = 0.65 * 100 = 65.0
        assert score == pytest.approx(65.0, rel=0.01)
    
    def test_equity_score_favors_low_income(self):
        """Test that equity score favors lower-income areas."""
        low_income_score = ScoringService.compute_equity_score(
            income_index=0.2,
            renters_share=0.5
        )
        
        high_income_score = ScoringService.compute_equity_score(
            income_index=0.8,
            renters_share=0.5
        )
        
        assert low_income_score > high_income_score
    
    def test_traffic_score_calculation(self):
        """Test traffic score computation."""
        score = ScoringService.compute_traffic_score(traffic_index=0.75)
        assert score == 75.0
    
    def test_grid_score_with_parking(self):
        """Test grid score with parking lot."""
        score = ScoringService.compute_grid_score(
            parking_lot_flag=1,
            municipal_parcel_flag=0
        )
        # Base 50 + parking 25 = 75
        assert score == 75.0
    
    def test_grid_score_with_municipal(self):
        """Test grid score with municipal parcel."""
        score = ScoringService.compute_grid_score(
            parking_lot_flag=0,
            municipal_parcel_flag=1
        )
        # Base 50 + municipal 15 = 65
        assert score == 65.0
    
    def test_grid_score_maxes_at_100(self):
        """Test that grid score doesn't exceed 100."""
        score = ScoringService.compute_grid_score(
            parking_lot_flag=1,
            municipal_parcel_flag=1
        )
        # Base 50 + parking 25 + municipal 15 = 90
        assert score == 90.0
        assert score <= 100.0
    
    def test_overall_score_calculation(self):
        """Test overall score as weighted combination."""
        score = ScoringService.compute_overall_score(
            score_demand=80.0,
            score_equity=60.0,
            score_grid=70.0
        )
        
        # Expected: 0.45*80 + 0.35*60 + 0.20*70 = 36 + 21 + 14 = 71.0
        assert score == pytest.approx(71.0, rel=0.01)
    
    def test_daily_kwh_estimate(self):
        """Test daily kWh demand estimation."""
        kwh = ScoringService.estimate_daily_kwh(
            traffic_index=0.7,
            pop_density_index=0.5
        )
        
        # Expected: (4 + 8*0.7 + 6*0.5) * 25 = (4 + 5.6 + 3) * 25 = 12.6 * 25 = 315
        assert kwh == pytest.approx(315.0, rel=0.01)
    
    def test_compute_all_scores(self):
        """Test computing all scores at once."""
        features = {
            'traffic_index': 0.8,
            'pop_density_index': 0.6,
            'renters_share': 0.5,
            'income_index': 0.4,
            'poi_index': 0.7,
            'parking_lot_flag': 1,
            'municipal_parcel_flag': 0,
        }
        
        results = ScoringService.compute_all_scores(features)
        
        # Check all required keys present
        assert 'score_demand' in results
        assert 'score_equity' in results
        assert 'score_traffic' in results
        assert 'score_grid' in results
        assert 'score_overall' in results
        assert 'daily_kwh_estimate' in results
        
        # Check values are in reasonable ranges
        assert 0 <= results['score_demand'] <= 100
        assert 0 <= results['score_equity'] <= 100
        assert 0 <= results['score_traffic'] <= 100
        assert 0 <= results['score_grid'] <= 100
        assert 0 <= results['score_overall'] <= 100
        assert results['daily_kwh_estimate'] > 0
    
    def test_compute_all_scores_with_defaults(self):
        """Test that missing features use defaults."""
        features = {
            'traffic_index': 0.5,
            # Other features missing
        }
        
        results = ScoringService.compute_all_scores(features)
        
        # Should not raise error and should return valid results
        assert isinstance(results, dict)
        assert 'score_overall' in results
