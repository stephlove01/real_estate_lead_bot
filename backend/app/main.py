"""
FastAPI application entrypoint for the Real Estate Lead Bot.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Real Estate Lead Bot API",
    description="API for PrimeHomes Realty lead capture, qualification, and management",
    version="0.1.0",
)

# CORS — will be driven by settings later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/health")
def health_check():
    """Simple health endpoint to verify the backend is running."""
    return {
        "status": "ok",
        "service": "real-estate-lead-bot",
        "version": "0.1.0",
    }


@app.get("/")
def root():
    return {
        "message": "Real Estate Lead Bot API",
        "docs": "/docs",
        "health": "/api/v1/health",
    }
