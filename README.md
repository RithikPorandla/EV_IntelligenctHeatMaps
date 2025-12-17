# MA EV ChargeMap

**EV Charging Siting Intelligence for Massachusetts**

A full-stack data science and engineering portfolio project that uses data analysis, machine learning, and interactive visualization to identify optimal locations for EV charging infrastructure.

![Portfolio Project Badge](https://img.shields.io/badge/Project-Portfolio-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-teal)
![Next.js](https://img.shields.io/badge/Next.js-14-black)

---

## 🎯 Project Overview

This project demonstrates end-to-end capabilities in:
- **Data Analysis**: Processing public datasets to extract insights
- **Data Engineering**: Building ETL pipelines with reproducible transformations
- **Machine Learning**: Training regression models to predict charging demand
- **Full-Stack Development**: FastAPI backend + Next.js frontend
- **Geospatial Visualization**: Interactive maps with heatmaps and site markers

### What It Does

MA EV ChargeMap analyzes candidate locations for EV charging stations in Massachusetts cities (starting with Worcester) using a multi-dimensional scoring system:

- **Demand Score**: Traffic patterns, population density, and points of interest
- **Equity Score**: Prioritizes underserved communities (lower-income areas, renters)
- **Traffic Score**: Direct traffic volume indicator
- **Grid Score**: Infrastructure readiness (parking lots, municipal properties)
- **Overall Score**: Weighted combination optimizing all factors

The system predicts expected daily charging demand (kWh) using a trained ML model and provides an interactive map interface for exploring opportunities.

---

## 🚀 Quick Start

### With Docker + Real Data (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd ma-ev-chargemap

# Download real data (optional but recommended)
cd data
python fetch_real_data.py  # 2-5 minutes, downloads from OSM & Census
cd ..

# Run setup script
chmod +x infra/dev-setup.sh
./infra/dev-setup.sh

# Access the application
# Frontend: http://localhost:3000
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

**See** [REAL_DATA_QUICKSTART.md](REAL_DATA_QUICKSTART.md) for detailed real data guide.

### Without Docker

#### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your database URL

# Initialize database
python -c "from app.database import init_db; init_db()"

# Run data pipeline (with optional real data)
cd ../data
python fetch_real_data.py  # Optional: Download real OSM & Census data
./run_pipeline.sh

# Start API
cd ../backend
python -m app.main
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment
cp .env.example .env.local
# Edit .env.local with your API URL

# Run development server
npm run dev
```

---

## 📊 Architecture

```
┌─────────────────┐
│   Frontend      │  Next.js + TypeScript + Tailwind
│   (Port 3000)   │  Interactive maps with React Leaflet
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│   Backend API   │  FastAPI + Python
│   (Port 8000)   │  REST endpoints, ML predictions
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   PostgreSQL    │  Site data, features, scores
│   (Port 5432)   │
└─────────────────┘

Data Pipeline (Python scripts)
├── ingest_parcels.py      → Generate candidate sites
├── ingest_demographics.py → Add demographic features
├── ingest_traffic.py      → Add traffic features
└── build_scores.py        → Compute final scores

ML Pipeline (Jupyter notebooks)
├── 01_eda_worcester.ipynb    → Exploratory data analysis
└── 02_model_training.ipynb   → Model training & export
```

---

## 🗂️ Project Structure

```
.
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes and schemas
│   │   ├── models/      # SQLAlchemy models
│   │   ├── services/    # Business logic (scoring, ML)
│   │   ├── config.py    # Configuration
│   │   ├── database.py  # Database connection
│   │   └── main.py      # FastAPI application
│   ├── config/          # Incentives data (JSON)
│   ├── tests/           # Backend tests
│   └── requirements.txt
│
├── frontend/            # Next.js frontend
│   ├── src/
│   │   ├── app/        # Pages (Next.js 14 App Router)
│   │   ├── components/ # React components
│   │   ├── lib/        # API client, utilities
│   │   └── types/      # TypeScript types
│   └── package.json
│
├── data/                # Data pipeline scripts
│   ├── ingest_parcels.py
│   ├── ingest_demographics.py
│   ├── ingest_traffic.py
│   ├── build_scores.py
│   └── run_pipeline.sh
│
├── notebooks/           # Jupyter notebooks
│   ├── 01_eda_worcester.ipynb
│   └── 02_model_training.ipynb
│
├── models/              # Trained ML models
│   └── site_score_model.pkl
│
├── docs/                # Documentation
│   ├── DATA_SOURCES.md
│   ├── SCORING_MODEL.md
│   ├── API.md
│   └── DATA_PIPELINE.md
│
├── infra/               # Infrastructure & setup
│   ├── dev-setup.sh
│   └── init-db.sh
│
└── docker-compose.yml   # Docker orchestration
```

---

## 🔑 Key Features

### Interactive Map Interface
- **OpenStreetMap base layer** with custom markers
- **Score-based color coding** (red → yellow → green)
- **Site popups** with quick information
- **Filterable views** by score type and minimum threshold

### Multi-Dimensional Scoring
- Transparent heuristic formulas (documented in code)
- Configurable weights for different priorities
- Support for "what-if" scenario analysis via API

### Machine Learning Integration
- Regression model predicts daily kWh demand
- Feature importance analysis in notebooks
- Model artifact exported for API deployment
- Fallback to heuristic if model unavailable

### Data Pipeline
- **Real data integration**: OpenStreetMap + US Census Bureau
- Modular Python scripts for each data source
- Reproducible transformations with automatic fallback
- Clear separation of raw → processed data
- Works with real OR synthetic data

---

## 📈 Scoring Model

### Heuristic Formulas

**Demand Score:**
```
score_demand = 0.4 × traffic + 0.3 × population + 0.3 × POI
```

**Equity Score:**
```
score_equity = 0.5 × (1 - income) + 0.5 × renters
```

**Overall Score:**
```
score_overall = 0.45 × demand + 0.35 × equity + 0.20 × grid
```

**Daily kWh Estimate:**
```
sessions = 4 + 8 × traffic + 6 × population
daily_kwh = sessions × 25 kWh/session
```

See [docs/SCORING_MODEL.md](docs/SCORING_MODEL.md) for detailed methodology.

---

## 🗄️ Data Sources

### ✨ Now with Real Open Data Integration!

The project can use **real, publicly available datasets**:

**Currently Integrated** (no authentication required):
- **OpenStreetMap**: Buildings, POIs, road network via Overpass API
- **US Census Bureau**: Demographics, income, housing data via public API

**Referenced for Enhancement**:
- **MassGIS Property Tax Parcels**: Detailed parcel data
- **MAPC DataCommon**: Regional demographics
- **MassDOT Traffic Inventory**: Actual traffic counts

### Getting Real Data

```bash
cd data
python fetch_real_data.py  # Downloads from OSM & Census (~5 min)
./run_pipeline.sh           # Automatically uses real data if available
```

**Fallback**: If real data unavailable, automatically uses synthetic data for demonstration.

See [data/README_REAL_DATA.md](data/README_REAL_DATA.md) for details.

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

Tests cover:
- Scoring logic validation
- API endpoint responses
- Input validation
- Edge cases

### Type Checking

```bash
# Backend
cd backend
mypy app/

# Frontend
cd frontend
npm run type-check
```

---

## 📚 API Documentation

The backend provides OpenAPI documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `GET /api/cities` - List supported cities
- `GET /api/sites?city=worcester` - Get all sites for a city
- `GET /api/sites/{id}` - Get detailed site info
- `POST /api/predict` - Predict scores for hypothetical location
- `GET /api/stats/{city}` - Get city statistics

See [docs/API.md](docs/API.md) for full API reference.

---

## 🎓 Skills Demonstrated

### Data Analysis
- Exploratory data analysis in Jupyter
- Feature engineering and normalization
- Correlation analysis
- Geospatial data processing

### Data Engineering
- ETL pipeline design
- Database schema design (SQLAlchemy ORM)
- Data quality and validation
- Reproducible data transformations

### Machine Learning
- Regression model training (scikit-learn)
- Feature importance analysis
- Cross-validation and evaluation
- Model serialization and deployment

### Full-Stack Development
- REST API design (FastAPI)
- Type-safe frontend (TypeScript)
- Responsive UI (Tailwind CSS)
- Interactive maps (React Leaflet)
- Docker containerization

---

## 🚧 Limitations & Future Work

### Current Limitations
1. **Data Coverage**: Uses OSM and Census (good coverage). Could enhance with MassDOT traffic counts and MAPC detailed layers.
2. **Single City**: Pilot focuses on Worcester. Framework supports expansion to other MA cities.
3. **Static Model**: ML model trained once. Production would include retraining pipeline.
4. **Simplified Grid Score**: Uses road proximity. Could integrate actual utility infrastructure data.

### Future Enhancements
1. **Enhanced Data**: MassDOT actual traffic counts, MAPC detailed demographics
2. **Temporal Predictions**: Time-of-day and seasonal demand forecasting
3. **Route Planning**: Optimal charger network topology
4. **Cost Analysis**: ROI calculator with utility rates and incentives
5. **User Accounts**: Save analyses, compare scenarios
6. **Mobile App**: Native mobile interface
7. **More Cities**: Expand to Boston, Cambridge, Springfield, etc.

---

## 🤝 Contributing

This is a personal portfolio project. However, feedback and suggestions are welcome via issues.

---

## 📄 License

This project is for portfolio and educational purposes.

Data sources are from Massachusetts public open data portals and remain subject to their respective licenses.

---

## 👤 About

**MA EV ChargeMap** is a solo developer portfolio project created to demonstrate:
- End-to-end data science and engineering capabilities
- Full-stack development skills
- Clean code practices and documentation
- Real-world problem-solving with public data

**Built with**: Python, FastAPI, PostgreSQL, TypeScript, Next.js, React, Tailwind CSS, Leaflet, scikit-learn, pandas

---

## 📞 Contact

- **GitHub**: [Your GitHub Profile]
- **LinkedIn**: [Your LinkedIn Profile]
- **Portfolio**: [Your Portfolio Website]

---

## 🙏 Acknowledgments

- Massachusetts Open Data Portal
- MassGIS and MAPC for data resources
- OpenStreetMap contributors
- FastAPI, Next.js, and all open-source libraries used

---

**⚡ Built to demonstrate data-driven decision making for sustainable transportation infrastructure.**
