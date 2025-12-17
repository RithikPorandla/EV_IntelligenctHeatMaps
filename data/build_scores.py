import sys
import os
import random

# Add backend to path to reuse models/logic
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

from app.services.scoring import ScoringService

def build_scores():
    print("Building scores for all candidates...")
    
    # Mock iterating over processed parcels
    candidates = []
    for i in range(10):
        # Mock features
        traffic = random.random()
        pop = random.random()
        
        scores = ScoringService.calculate_scores(
            traffic_index=traffic,
            pop_density_index=pop,
            renters_share=random.random(),
            income_index=random.random(),
            poi_index=random.random()
        )
        
        candidates.append({
            "id": i,
            "scores": scores
        })
    
    print(f"Computed scores for {len(candidates)} sites.")
    print("In a real run, these would be upserted to the Postgres DB.")

if __name__ == "__main__":
    build_scores()
