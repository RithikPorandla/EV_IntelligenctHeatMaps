"""
ML prediction service for EV charging demand estimation.

This service loads a trained scikit-learn model and provides
predictions for new candidate locations.
"""
import pickle
import os
from typing import Dict, Optional
import numpy as np


class MLPredictor:
    """
    Service for loading and using trained ML models.
    
    The model predicts daily kWh demand based on site features.
    If no model is available, falls back to heuristic estimation.
    """
    
    def __init__(self, model_path: str = "models/site_score_model.pkl"):
        """
        Initialize predictor and load model if available.
        
        Args:
            model_path: Path to pickled scikit-learn model
        """
        self.model_path = model_path
        self.model = None
        self.feature_names = [
            'traffic_index',
            'pop_density_index',
            'renters_share',
            'income_index',
            'poi_index',
            'parking_lot_flag',
            'municipal_parcel_flag'
        ]
        
        # Try to load model
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print(f"✓ Loaded ML model from {model_path}")
            except Exception as e:
                print(f"⚠ Failed to load model: {e}")
                self.model = None
        else:
            print(f"ℹ No model found at {model_path}, will use heuristic fallback")
    
    def predict_daily_kwh(self, features: Dict[str, float]) -> float:
        """
        Predict daily kWh demand for a site.
        
        Args:
            features: Dictionary of site features
        
        Returns:
            Predicted daily kWh demand
        """
        if self.model is None:
            # Fallback to heuristic
            return self._heuristic_estimate(features)
        
        try:
            # Prepare feature vector in correct order
            feature_vector = np.array([
                [features.get(name, 0.0) for name in self.feature_names]
            ])
            
            # Predict
            prediction = self.model.predict(feature_vector)[0]
            
            # Ensure reasonable bounds
            return max(0.0, min(prediction, 1000.0))
            
        except Exception as e:
            print(f"⚠ Prediction failed: {e}, using heuristic")
            return self._heuristic_estimate(features)
    
    def _heuristic_estimate(self, features: Dict[str, float]) -> float:
        """
        Fallback heuristic estimation when ML model unavailable.
        
        Args:
            features: Dictionary of site features
        
        Returns:
            Estimated daily kWh demand
        """
        traffic_index = features.get('traffic_index', 0.0)
        pop_density_index = features.get('pop_density_index', 0.0)
        
        # Simple linear model
        sessions = 4.0 + 8.0 * traffic_index + 6.0 * pop_density_index
        kwh_per_session = 25.0
        
        return sessions * kwh_per_session
    
    def get_model_info(self) -> Dict[str, any]:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary with model metadata
        """
        if self.model is None:
            return {
                "model_loaded": False,
                "model_type": "heuristic_fallback",
                "message": "Using heuristic estimation"
            }
        
        return {
            "model_loaded": True,
            "model_type": type(self.model).__name__,
            "feature_names": self.feature_names,
            "model_path": self.model_path
        }


# Global predictor instance
predictor = MLPredictor()
