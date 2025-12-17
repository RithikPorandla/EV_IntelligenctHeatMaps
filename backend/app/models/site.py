"""
Database model for candidate EV charging sites.
"""
from sqlalchemy import Column, Integer, Float, String, Index
from app.database import Base


class Site(Base):
    """
    Represents a candidate location for EV charging infrastructure.
    
    Each site has geographic coordinates, computed scores across multiple
    dimensions (demand, equity, traffic, grid), and an estimated daily
    charging demand in kWh.
    """
    __tablename__ = "sites"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Location
    city = Column(String, nullable=False, index=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    location_label = Column(String, nullable=True)  # e.g., "Near Main St & Park Ave"
    parcel_id = Column(String, nullable=True)
    
    # Feature indexes (0-1 normalized)
    traffic_index = Column(Float, default=0.0)
    pop_density_index = Column(Float, default=0.0)
    renters_share = Column(Float, default=0.0)
    income_index = Column(Float, default=0.0)
    poi_index = Column(Float, default=0.0)
    parking_lot_flag = Column(Integer, default=0)
    municipal_parcel_flag = Column(Integer, default=0)
    
    # Computed scores (0-100)
    score_demand = Column(Float, nullable=False)
    score_equity = Column(Float, nullable=False)
    score_traffic = Column(Float, nullable=False)
    score_grid = Column(Float, nullable=False)
    score_overall = Column(Float, nullable=False)
    
    # Predicted daily charging demand
    daily_kwh_estimate = Column(Float, nullable=False)
    
    # Add indexes for common queries
    __table_args__ = (
        Index('idx_city_score', 'city', 'score_overall'),
        Index('idx_location', 'lat', 'lng'),
    )
    
    def to_dict(self):
        """Convert site to dictionary for API responses."""
        return {
            "id": self.id,
            "city": self.city,
            "lat": self.lat,
            "lng": self.lng,
            "location_label": self.location_label,
            "parcel_id": self.parcel_id,
            "features": {
                "traffic_index": round(self.traffic_index, 3),
                "pop_density_index": round(self.pop_density_index, 3),
                "renters_share": round(self.renters_share, 3),
                "income_index": round(self.income_index, 3),
                "poi_index": round(self.poi_index, 3),
                "parking_lot_flag": self.parking_lot_flag,
                "municipal_parcel_flag": self.municipal_parcel_flag,
            },
            "scores": {
                "demand": round(self.score_demand, 1),
                "equity": round(self.score_equity, 1),
                "traffic": round(self.score_traffic, 1),
                "grid": round(self.score_grid, 1),
                "overall": round(self.score_overall, 1),
            },
            "daily_kwh_estimate": round(self.daily_kwh_estimate, 1),
        }
    
    def to_geojson_feature(self):
        """Convert site to GeoJSON feature for map visualization."""
        score_amenities = round(self.poi_index * 100.0, 1)
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [self.lng, self.lat]
            },
            "properties": {
                "id": self.id,
                "city": self.city,
                "location_label": self.location_label,
                "score_overall": round(self.score_overall, 1),
                "score_demand": round(self.score_demand, 1),
                "score_equity": round(self.score_equity, 1),
                "score_traffic": round(self.score_traffic, 1),
                "score_grid": round(self.score_grid, 1),
                "score_amenities": score_amenities,
                "daily_kwh_estimate": round(self.daily_kwh_estimate, 1),
                "parking_lot_flag": self.parking_lot_flag,
                "municipal_parcel_flag": self.municipal_parcel_flag,
            }
        }
