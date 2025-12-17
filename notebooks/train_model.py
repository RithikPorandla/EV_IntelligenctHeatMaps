import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

# 1. Generate Synthetic Data
# We want to predict 'daily_kwh_demand' based on site features.

np.random.seed(42)
n_samples = 1000

data = {
    'traffic_index': np.random.uniform(0, 1, n_samples),
    'pop_density_index': np.random.uniform(0, 1, n_samples),
    'renters_share': np.random.uniform(0, 1, n_samples),
    'income_index': np.random.uniform(0, 1, n_samples),
    'poi_index': np.random.uniform(0, 1, n_samples),
}

df = pd.DataFrame(data)

# Define a "ground truth" formula with some noise
# Demand is higher with traffic, population, and POI density.
# Slightly lower if income is very low (maybe less EV adoption currently, though equity score tries to balance this).
df['daily_kwh'] = (
    4.0 + 
    8.0 * df['traffic_index'] + 
    6.0 * df['pop_density_index'] + 
    3.0 * df['poi_index'] + 
    2.0 * df['income_index'] +
    np.random.normal(0, 1.5, n_samples) # Noise
) * 25.0 # avg kWh per session

# 2. Train Model
X = df[['traffic_index', 'pop_density_index', 'renters_share', 'income_index', 'poi_index']]
y = df['daily_kwh']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training RandomForestRegressor...")
model = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# 3. Evaluate
preds = model.predict(X_test)
mse = mean_squared_error(y_test, preds)
r2 = r2_score(y_test, preds)

print(f"Model Evaluation:")
print(f"MSE: {mse:.2f}")
print(f"R2 Score: {r2:.2f}")

# 4. Save Model
model_path = 'models/site_score_model.pkl'
os.makedirs(os.path.dirname(model_path), exist_ok=True)
joblib.dump(model, model_path)
print(f"Model saved to {model_path}")
