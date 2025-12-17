# MA EV ChargeMap - Prototype

Interactive siting intelligence for EV charging infrastructure in Massachusetts Gateway Cities (starting with Worcester).

## Project Structure

- `/backend`: FastAPI Python application
- `/frontend`: Next.js React application
- `/data`: ETL scripts and data processing
- `/infra`: Docker infrastructure configuration
- `/docs`: Detailed documentation

## Getting Started

### Prerequisites

- Docker & Docker Compose

### Running with Docker

1. Navigate to infra:
   ```bash
   cd infra
   ```
2. Start services:
   ```bash
   docker-compose up --build
   ```
3. Access the application:
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8000/docs](http://localhost:8000/docs)

### Manual Setup

See `backend/README.md` and `frontend/README.md` (if they existed) for individual setup, but generally:

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Features

- **Interactive Heatmap**: Visualizes demand, equity, and traffic scores.
- **Site Details**: Click on any point to see detailed metrics and estimated grid impact.
- **Scoring Engine**: Transparent heuristic model for site ranking.

## Data

The system uses a mock dataset for Worcester generated on startup if the database is empty.
To ingest real data, use the scripts in `/data`.
