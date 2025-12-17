import os
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.site import Base, Site
from app.services.scoring import ScoringService

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/evmap")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Check if we have data, if not, seed some dummy data for Worcester
    db = SessionLocal()
    if db.query(Site).count() == 0:
        print("Seeding database with mock Worcester data...")
        seed_worcester_data(db)
    db.close()

def seed_worcester_data(db):
    """
    Generates a grid of points around Worcester, MA center.
    Center approx: 42.2626, -71.8023
    """
    center_lat = 42.2626
    center_lng = -71.8023
    
    # Generate ~100 points
    for i in range(100):
        # Random offset
        lat = center_lat + random.uniform(-0.04, 0.04)
        lng = center_lng + random.uniform(-0.06, 0.06)
        
        # Random inputs
        traffic = random.random()
        pop = random.random()
        renter = random.random()
        income = random.uniform(0.2, 0.9) # Less likely to be 0 or 1
        poi = random.random()
        
        scores = ScoringService.calculate_scores(
            traffic_index=traffic,
            pop_density_index=pop,
            renters_share=renter,
            income_index=income,
            poi_index=poi
        )
        
        daily_kwh = ScoringService.estimate_daily_kwh(traffic, pop)
        
        site = Site(
            city_slug="worcester",
            parcel_id=f"W-{i:04d}",
            address=f"Mock Address {i}",
            lat=lat,
            lng=lng,
            traffic_index=traffic,
            pop_density_index=pop,
            renters_share=renter,
            income_index=income,
            poi_index=poi,
            score_demand=scores["score_demand"],
            score_equity=scores["score_equity"],
            score_traffic=scores["score_traffic"],
            score_grid=scores["score_grid"],
            score_overall=scores["score_overall"],
            daily_kwh_estimate=daily_kwh
        )
        db.add(site)
    
    db.commit()
