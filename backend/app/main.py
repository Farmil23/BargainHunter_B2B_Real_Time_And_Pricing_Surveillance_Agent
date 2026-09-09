from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import logging

from fastapi.responses import StreamingResponse
import io

from backend.app.core.config import settings
from backend.app.api.routes import surveillance
from backend.app.db.session import engine, Base
from backend.app.models import domain
from backend.app.services.scheduler import start_scheduler, stop_scheduler
from backend.app.agents.workflows import surveillance_app


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

@app.get("/graph", response_class=Response)
async def get_graph_image():
    """
    Endpoint untuk mengambil gambar visualisasi LangGraph dalam format PNG.
    """
    try:
        # 1. Ambil biner gambar PNG dari LangGraph
        # Pastikan 'langgraph_app' adalah graf yang sudah di-compile (workflow.compile())
        png_bytes = surveillance_app.get_graph().draw_mermaid_png()
        
        # 2. Kembalikan sebagai respon gambar PNG
        return Response(content=png_bytes, media_type="image/png")
        
    except Exception as e:
        return {"error": f"Gagal membuat gambar graf: {str(e)}"}