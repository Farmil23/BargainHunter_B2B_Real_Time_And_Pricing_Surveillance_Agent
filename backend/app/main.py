from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from backend.app.core.config import settings
from backend.app.api.routes import surveillance
from backend.app.db.session import engine, Base
from backend.app.models import domain
from backend.app.services.scheduler import start_scheduler, stop_scheduler
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend API for Real-Time Market & Pricing Surveillance Agent"
)

# Auto-create database tables (Hibernate auto-update equivalent)
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def on_startup():
    start_scheduler()

@app.on_event("shutdown")
def on_shutdown():
    stop_scheduler()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"],
)

@app.middleware("http")
async def add_ngrok_skip_header(request, call_next):
    response = await call_next(request)
    # Menambahkan header ini membantu dalam beberapa kasus CORS dengan ngrok
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

# Include routers
app.include_router(surveillance.router, prefix="/api/v1/surveillance", tags=["Surveillance"])

@app.get("/health")
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}
