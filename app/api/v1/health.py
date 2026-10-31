from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(tags=["Health & Status"])


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Sorateq AI Backend & RAG Orchestrator",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "features": {
            "pgvector": True,
            "hybrid_search": True,
            "model_routing": True,
            "sse_streaming": True
        }
    }
