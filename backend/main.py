"""
FastAPI main application entry point
Hackathon version - simplified for demo
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="ScholarLens API - Hackathon Demo",
    description="Adaptive Scholarship Matching + AI Drafting - Demo Version",
    version="1.0.0-hackathon",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware - allow all for hackathon demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """
    Health check endpoint
    """
    return {
        "status": "ok",
        "message": "ScholarLens Hackathon API is running",
        "version": "1.0.0-hackathon",
        "docs": "/docs",
        "demo_endpoints": "/demo"
    }


@app.get("/health")
def health_check():
    """
    Health check for monitoring
    """
    return {"status": "healthy"}


# Import routes
from api.routes import demo, profiles

# Register routers
app.include_router(demo.router, prefix="/api/v1", tags=["Demo"])
app.include_router(profiles.router, prefix="/api/v1", tags=["Profiles"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
