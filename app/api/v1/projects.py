from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.models import Project
from app.services.rag_service import RAGService

router = APIRouter(prefix="/projects", tags=["Projects Catalog"])


@router.get("")
async def get_projects(
    industry: Optional[str] = None,
    limit: int = Query(50, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    List all public projects with optional industry filtering.
    """
    stmt = select(Project).where(Project.visibility == "PUBLIC")
    if industry:
        stmt = stmt.where(Project.industry.ilike(f"%{industry}%"))
    stmt = stmt.limit(limit)
    res = await db.execute(stmt)
    projects = res.scalars().all()
    return {"status": "success", "count": len(projects), "projects": projects}


@router.get("/search")
async def search_projects(
    q: str = Query(..., min_length=1),
    industry: Optional[str] = None,
    limit: int = Query(6, le=20),
    db: AsyncSession = Depends(get_db)
):
    """
    Semantic & hybrid search across projects using pgvector.
    """
    rag = RAGService(db)
    results = await rag.search_projects(query=q, limit=limit, industry=industry, visibility="PUBLIC")
    return {"status": "success", "query": q, "results": results}


@router.get("/{slug}")
async def get_project_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed project case study by slug.
    """
    stmt = select(Project).where(Project.slug == slug, Project.visibility == "PUBLIC")
    res = await db.execute(stmt)
    proj = res.scalar_one_or_none()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"status": "success", "project": proj}
