import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.chat import ChatMessageRequest
from app.services.sora_engine import SoraEngine
from app.services.brief_generator import BriefGenerator

router = APIRouter(prefix="/chat", tags=["Sora Chat"])


@router.post("/stream")
async def stream_sora_chat(
    payload: ChatMessageRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    SSE Streaming endpoint for Sora conversations with real-time token delivery and RAG context.
    """
    engine = SoraEngine(db)
    
    return StreamingResponse(
        engine.generate_response_stream(
            message=payload.message,
            conversation_history=payload.history or [],
            current_profile=payload.current_profile or {},
            current_state=payload.context_state or "NEW",
            question_count=payload.question_count or 0,
        ),
        media_type="text/event-stream"
    )


@router.post("/brief")
async def generate_project_brief(
    payload: dict
):
    """
    Generates a structured project brief from profile information.
    """
    brief = BriefGenerator.generate_brief(payload.get("profile", {}))
    return {"status": "success", "brief": brief}
