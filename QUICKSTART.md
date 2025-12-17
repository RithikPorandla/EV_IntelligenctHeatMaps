# Quick Start Guide

Get MA EV ChargeMap running in under 5 minutes!

---

## Prerequisites

- Docker & Docker Compose installed
- 4GB RAM available
- 2GB disk space

---

## Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd ma-ev-chargemap

# Run automated setup
chmod +x infra/dev-setup.sh
./infra/dev-setup.sh
```

**This will:**
1. ✅ Build Docker images
2. ✅ Start all services (database, backend, frontend)
3. ✅ Run data pipeline to generate Worcester sites
4. ✅ Everything ready at:
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

---

## Option 2: Manual Docker Setup

```bash
# Clone repository
git clone <your-repo-url>
cd ma-ev-chargemap

# Create environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# Start services
docker-compose up -d

# Wait for services to start (30 seconds)
sleep 30

# Run data pipeline
docker-compose exec backend bash -c "
    python ../data/ingest_parcels.py &&
    python ../data/ingest_demographics.py &&
    python ../data/ingest_traffic.py &&
    python ../data/build_scores.py
"

# Done! Access at http://localhost:3000
```

---

## Option 3: Local Development (No Docker)

### Backend

```bash
# Install PostgreSQL 15+
# Create database: createdb evcharge

cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database URL

# Initialize database
python -c "from app.database import init_db; init_db()"

# Run data pipeline
cd ../data
./run_pipeline.sh

# Start API
cd ../backend
python -m app.main
```

Backend running at: http://localhost:8000

### Frontend

```bash
# Install Node.js 18+

cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local to point to backend

# Start dev server
npm run dev
```

Frontend running at: http://localhost:3000

---

## Verify Installation

1. **Backend API**:
   ```bash
   curl http://localhost:8000/api/health
   # Should return: {"status":"healthy",...}
   ```

2. **Check data**:
   ```bash
   curl http://localhost:8000/api/cities
   # Should return Worcester city info
   ```

3. **Frontend**:
   - Open http://localhost:3000
   - Should see landing page
   - Click "Explore Worcester Map"
   - Should see interactive map with sites

---

## Common Issues

### "Database connection failed"
- Ensure PostgreSQL is running
- Check DATABASE_URL in backend/.env
- For Docker: `docker-compose ps` should show db as "Up"

### "No sites found"
- Run data pipeline: `cd data && ./run_pipeline.sh`
- Check database: `docker-compose exec db psql -U evcharge -c "SELECT COUNT(*) FROM sites;"`

### "Cannot connect to API"
- Backend not started? Check: `curl http://localhost:8000/api/health`
- Check NEXT_PUBLIC_API_URL in frontend/.env.local

### Port already in use
- Change ports in docker-compose.yml
- Or stop conflicting services

---

## Next Steps

1. **Explore the Map**:
   - Try different score types (demand, equity, traffic)
   - Adjust minimum score filter
   - Click on sites for details

2. **Try the API**:
   - Visit http://localhost:8000/docs
   - Try the `/api/predict` endpoint
   - Experiment with different feature values

3. **View the Notebooks**:
   ```bash
   cd notebooks
   jupyter notebook
   # Open 01_eda_worcester.ipynb
   ```

4. **Read the Documentation**:
   - [docs/SCORING_MODEL.md](docs/SCORING_MODEL.md) - How scoring works
   - [docs/API.md](docs/API.md) - Complete API reference
   - [docs/DATA_PIPELINE.md](docs/DATA_PIPELINE.md) - Data processing

---

## Stopping Services

### Docker
```bash
docker-compose down
```

### Local
- Backend: Ctrl+C in terminal
- Frontend: Ctrl+C in terminal
- PostgreSQL: `sudo systemctl stop postgresql` (or your system's method)

---

## Troubleshooting

**Get logs:**
```bash
# Docker
docker-compose logs -f backend
docker-compose logs -f frontend

# Local
# Check terminal output where services are running
```

**Reset everything:**
```bash
# Docker
docker-compose down -v  # -v removes volumes (database data)
./infra/dev-setup.sh    # Restart fresh

# Local
dropdb evcharge         # Delete database
createdb evcharge       # Recreate
# Re-run setup steps
```

**Get help:**
- Open an issue on GitHub
- Check existing issues for solutions

---

## Success! 🎉

You now have:
- ✅ Interactive map at http://localhost:3000
- ✅ REST API at http://localhost:8000
- ✅ ~500+ scored Worcester sites
- ✅ Complete portfolio project ready to show

**Next**: Take screenshots, update your resume, and share on LinkedIn! 🚀
