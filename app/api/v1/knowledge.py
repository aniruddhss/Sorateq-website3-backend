from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.models import KnowledgeItem
from app.services.rag_service import RAGService

router = APIRouter(prefix="/knowledge", tags=["Knowledge Base & RAG"])


@router.get("/search")
async def search_knowledge(
    q: str = Query(..., min_length=1),
    category: Optional[str] = None,
    limit: int = Query(5, le=20),
    db: AsyncSession = Depends(get_db)
):
    """
    RAG hybrid retrieval across company knowledge base enforcing PUBLIC visibility.
    """
    rag = RAGService(db)
    results = await rag.search_knowledge(query=q, category=category, limit=limit, visibility="PUBLIC")
    return {"status": "success", "query": q, "results": results}


@router.get("/categories")
async def get_categories(
    db: AsyncSession = Depends(get_db)
):
    """
    List available public knowledge categories.
    """
    stmt = select(KnowledgeItem.category).where(KnowledgeItem.visibility == "PUBLIC").distinct()
    res = await db.execute(stmt)
    categories = [r[0] for r in res.all()]
    return {"status": "success", "categories": categories}
