from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from backend.app.core.config import settings
from backend.app.api.routes import surveillance

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend API for Real-Time Market & Pricing Surveillance Agent"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(surveillance.router, prefix="/api/v1/surveillance", tags=["Surveillance"])

@app.get("/health")
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}
