#!/bin/bash

# Development environment setup script
# Sets up the complete local development environment

set -e

echo "=========================================="
echo "MA EV ChargeMap - Development Setup"
echo "=========================================="
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

echo "✓ Docker and docker-compose are installed"
echo ""

# Create .env files if they don't exist
echo "Setting up environment files..."

if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "✓ Created backend/.env"
fi

if [ ! -f frontend/.env.local ]; then
    cp frontend/.env.example frontend/.env.local
    echo "✓ Created frontend/.env.local"
fi

echo ""
echo "Building Docker images..."
docker-compose build

echo ""
echo "Starting services..."
docker-compose up -d

echo ""
echo "Waiting for services to be ready..."
sleep 10

echo ""
echo "Running data pipeline..."
docker-compose exec backend bash -c "cd /app && python -m pip install -e . 2>/dev/null || true"

# Run pipeline inside container
docker-compose exec backend bash -c "
    cd /app &&
    python /app/../data/ingest_parcels.py &&
    python /app/../data/ingest_demographics.py &&
    python /app/../data/ingest_traffic.py &&
    python /app/../data/build_scores.py
" || echo "⚠️  Data pipeline failed. You may need to run it manually."

echo ""
echo "=========================================="
echo "✓ Setup complete!"
echo "=========================================="
echo ""
echo "Services running at:"
echo "  - Frontend: http://localhost:3000"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Database: localhost:5432"
echo ""
echo "Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop services: docker-compose down"
echo "  - Restart: docker-compose restart"
echo ""
