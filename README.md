# MA EV ChargeMap – EV Charging Siting Intelligence for Massachusetts

**Personal Portfolio Project**

This project demonstrates a full-stack data & ML application designed to identify optimal locations for electric vehicle (EV) charging stations in Massachusetts cities, starting with a pilot in Worcester.

## Features

- **Interactive Map**: Visualize "EV Charging Opportunity Scores" across the city.
- **Multi-Factor Analysis**: Scores based on Charging Demand, Equity (environmental justice), and Traffic patterns.
- **Machine Learning Integration**: Predicts expected daily kWh demand using a RandomForest regressor trained on synthetic site data.
- **Modern Tech Stack**: Built with Next.js, FastAPI, and Python Data Stack.

## Tech Stack

- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, React Leaflet.
- **Backend**: FastAPI, Python 3.11.
- **Data & ML**: pandas, scikit-learn, joblib.
- **Infrastructure**: Docker support (planned).

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+

### Running the Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at http://localhost:8000.

### Running the Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   Open http://localhost:3000 in your browser.

## Project Structure

- `/backend`: FastAPI application and API endpoints.
- `/frontend`: Next.js web application.
- `/data`: Data ingestion and processing scripts.
- `/notebooks`: EDA and Model Training notebooks/scripts.
- `/docs`: Detailed documentation.

## Documentation

- [Data Sources](docs/DATA_SOURCES.md)
- [Scoring Model & ML](docs/SCORING_MODEL.md)
- [API Reference](docs/API.md)
- [Data Pipeline](docs/DATA_PIPELINE.md)
