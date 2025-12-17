"""
Score computation for all candidate sites.

This script computes all opportunity scores for each site based on
the ingested features. This is the final step in the data pipeline.

Scores computed:
- Demand score (0-100)
- Equity score (0-100)
- Traffic score (0-100)
- Grid score (0-100)
- Overall score (0-100)
- Daily kWh estimate
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.site import Site
from app.services.scoring import ScoringService
from app.config import settings


def main():
    """
    Compute scores for all sites.
    """
    print("📊 Computing scores for Worcester sites...")
    
    # Connect to database
    engine = create_engine(settings.database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Get all Worcester sites
    sites = session.query(Site).filter(Site.city == 'worcester').all()
    print(f"Processing {len(sites)} sites...")
    
    if len(sites) == 0:
        print("⚠️  No sites found. Run previous pipeline steps first.")
        return
    
    # Check if sites have features
    sample_site = sites[0]
    if sample_site.traffic_index == 0 and sample_site.pop_density_index == 0:
        print("⚠️  Sites missing features. Run ingest_demographics.py and ingest_traffic.py first.")
        return
    
    # Compute scores for each site
    for idx, site in enumerate(sites):
        # Prepare features dictionary
        features = {
            'traffic_index': site.traffic_index,
            'pop_density_index': site.pop_density_index,
            'renters_share': site.renters_share,
            'income_index': site.income_index,
            'poi_index': site.poi_index,
            'parking_lot_flag': site.parking_lot_flag,
            'municipal_parcel_flag': site.municipal_parcel_flag,
        }
        
        # Compute all scores
        scores = ScoringService.compute_all_scores(features)
        
        # Update site
        site.score_demand = round(scores['score_demand'], 1)
        site.score_equity = round(scores['score_equity'], 1)
        site.score_traffic = round(scores['score_traffic'], 1)
        site.score_grid = round(scores['score_grid'], 1)
        site.score_overall = round(scores['score_overall'], 1)
        site.daily_kwh_estimate = round(scores['daily_kwh_estimate'], 1)
        
        if (idx + 1) % 100 == 0:
            print(f"  Processed {idx + 1}/{len(sites)} sites")
    
    # Commit changes
    print("Saving to database...")
    session.commit()
    
    # Print summary statistics
    print("\n📈 Score Summary Statistics:")
    print(f"  Total sites: {len(sites)}")
    
    overall_scores = [s.score_overall for s in sites]
    demands = [s.daily_kwh_estimate for s in sites]
    
    print(f"\n  Overall Score:")
    print(f"    Min:  {min(overall_scores):.1f}")
    print(f"    Max:  {max(overall_scores):.1f}")
    print(f"    Mean: {sum(overall_scores) / len(overall_scores):.1f}")
    
    print(f"\n  Daily kWh Estimate:")
    print(f"    Total: {sum(demands):,.0f} kWh/day")
    print(f"    Mean:  {sum(demands) / len(demands):.1f} kWh/day per site")
    
    # Top 10 sites
    top_sites = sorted(sites, key=lambda s: s.score_overall, reverse=True)[:10]
    print(f"\n  🏆 Top 10 Sites by Overall Score:")
    for i, site in enumerate(top_sites, 1):
        print(f"    {i}. {site.location_label}: {site.score_overall:.1f} ({site.daily_kwh_estimate:.0f} kWh/day)")
    
    print("\n✓ Score computation complete")
    
    session.close()


if __name__ == "__main__":
    main()
