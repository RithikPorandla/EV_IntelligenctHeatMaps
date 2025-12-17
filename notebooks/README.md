# Analysis Notebooks

This directory contains Jupyter notebooks for data exploration and model training.

## Notebooks

### 01_eda_worcester.ipynb
Exploratory data analysis of Worcester candidate sites:
- Feature distributions
- Score correlations
- Spatial visualization
- Top opportunity sites
- Demand and equity analysis

### 02_model_training.ipynb
ML model development for charging demand prediction:
- Model comparison (Linear Regression, Random Forest, Gradient Boosting)
- Feature importance analysis
- Cross-validation
- Model export for API deployment

## Running the Notebooks

1. Set up the Python environment:
```bash
cd ../backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install jupyter matplotlib seaborn
```

2. Run the data pipeline first:
```bash
cd ../data
./run_pipeline.sh
```

3. Start Jupyter:
```bash
cd ../notebooks
jupyter notebook
```

4. Open and run notebooks in order (01, then 02).

## Requirements

- Completed data pipeline (sites in database)
- Python 3.9+
- All packages from `backend/requirements.txt`
- Additional: jupyter, matplotlib, seaborn
