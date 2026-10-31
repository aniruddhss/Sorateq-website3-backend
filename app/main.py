import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sorateq AI Backend & RAG Orchestrator",
    description="Production FastAPI backend with Supabase/PostgreSQL pgvector, hybrid search, Sora conversational engine, and Alembic migrations.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware: allow configured origins + any Render / Vercel deployment preview
origins = settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.onrender\.com|https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount v1 router
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Sorateq AI Orchestrator API is running",
        "docs": "/docs",
        "health": "/health",
        "api_health": "/api/v1/health"
    }


@app.get("/health")
async def health():
    """
    Standard top-level healthcheck endpoint for Render, Fly, and Docker monitors.
    """
    return {
        "status": "healthy",
        "service": "Sorateq AI Backend",
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", settings.BACKEND_PORT))
    uvicorn.run(
        "app.main:app",
        host=settings.BACKEND_HOST,
        port=port,
        reload=False
    )
