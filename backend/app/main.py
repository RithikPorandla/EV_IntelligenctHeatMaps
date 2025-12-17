"""
Main FastAPI application for MA EV ChargeMap.

This is a personal portfolio project demonstrating:
- Data analysis and engineering skills
- ML model deployment
- Full-stack API development
- Clean code and documentation practices
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.api.routes import router

# Create FastAPI application
app = FastAPI(
    title=settings.project_name,
    description=settings.project_description,
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """
    Initialize application on startup.
    
    Creates database tables if they don't exist.
    """
    print("🚀 Starting MA EV ChargeMap API...")
    print(f"📊 Version: {settings.version}")
    print(f"🔧 Debug mode: {settings.debug}")
    
    # Initialize database
    try:
        init_db()
        print("✓ Database initialized")
    except Exception as e:
        print(f"⚠ Database initialization warning: {e}")


@app.get("/")
def root():
    """
    Root endpoint with API information.
    """
    return {
        "name": settings.project_name,
        "version": settings.version,
        "description": settings.project_description,
        "docs": "/docs",
        "api_endpoints": {
            "cities": "/api/cities",
            "sites": "/api/sites?city=worcester",
            "predict": "/api/predict",
            "health": "/api/health",
        },
        "portfolio_note": (
            "This is a personal portfolio project by a solo developer, "
            "demonstrating data analysis, data engineering, ML, and full-stack skills."
        )
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
