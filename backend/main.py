from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import api

app = FastAPI(
    title="MA EV ChargeMap API",
    description="API for EV Charging Siting Intelligence in Massachusetts",
    version="0.1.0"
)

# Configure CORS for frontend
origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to MA EV ChargeMap API. Visit /docs for OpenAPI specifications."}
