import logging
from typing import List, Dict, Any, Optional
from sqlalchemy import select, or_, and_, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Project, KnowledgeItem
from app.services.embeddings import get_embedding

logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def search_projects(
        self,
        query: str,
        limit: int = 4,
        industry: Optional[str] = None,
        visibility: str = "PUBLIC"
    ) -> List[Dict[str, Any]]:
        """
        Hybrid search across projects using semantic embeddings and metadata filtering.
        Strictly enforces visibility level (e.g. PUBLIC only for visitors).
        """
        query_embedding = await get_embedding(query)
        results = []

        try:
            # Vector cosine distance search with metadata filter
            stmt = select(Project).where(Project.visibility == visibility)
            if industry:
                stmt = stmt.where(Project.industry.ilike(f"%{industry}%"))

            # Order by cosine distance if embeddings exist
            stmt = stmt.order_by(Project.embedding.cosine_distance(query_embedding)).limit(limit)
            exec_res = await self.db.execute(stmt)
            projects = exec_res.scalars().all()

            for p in projects:
                results.append({
                    "id": p.id,
                    "slug": p.slug,
                    "name": p.name,
                    "tagline": p.tagline,
                    "summary": p.summary,
                    "industry": p.industry,
                    "project_type": p.project_type,
                    "technologies": p.technologies or [],
                    "metrics": p.metrics or [],
                    "proof": p.proof,
                    "project_outcome": p.project_outcome,
                    "public_url": p.public_url,
                    "featured": p.featured
                })
        except Exception as e:
            logger.warning(f"Vector search failed, falling back to keyword ILIKE search: {e}")
            # Fallback keyword match
            keywords = [w.strip() for w in query.lower().split() if len(w.strip()) > 2]
            filters = [Project.visibility == visibility]
            if keywords:
                text_filters = []
                for kw in keywords[:4]:
                    text_filters.append(Project.name.ilike(f"%{kw}%"))
                    text_filters.append(Project.summary.ilike(f"%{kw}%"))
                    text_filters.append(Project.industry.ilike(f"%{kw}%"))
                filters.append(or_(*text_filters))

            stmt = select(Project).where(and_(*filters)).limit(limit)
            exec_res = await self.db.execute(stmt)
            projects = exec_res.scalars().all()
            for p in projects:
                results.append({
                    "id": p.id,
                    "slug": p.slug,
                    "name": p.name,
                    "tagline": p.tagline,
                    "summary": p.summary,
                    "industry": p.industry,
                    "project_type": p.project_type,
                    "technologies": p.technologies or [],
                    "metrics": p.metrics or [],
                    "proof": p.proof,
                    "project_outcome": p.project_outcome,
                    "public_url": p.public_url,
                    "featured": p.featured
                })

        return results

    async def search_knowledge(
        self,
        query: str,
        limit: int = 5,
        category: Optional[str] = None,
        visibility: str = "PUBLIC"
    ) -> List[Dict[str, Any]]:
        """
        Retrieves company knowledge, capabilities, methodology, architecture, and FAQs.
        Strictly enforces visibility level (never leaks INTERNAL/PRIVATE data).
        """
        query_embedding = await get_embedding(query)
        results = []

        try:
            stmt = select(KnowledgeItem).where(KnowledgeItem.visibility == visibility)
            if category:
                stmt = stmt.where(KnowledgeItem.category == category)

            stmt = stmt.order_by(KnowledgeItem.embedding.cosine_distance(query_embedding)).limit(limit)
            exec_res = await self.db.execute(stmt)
            items = exec_res.scalars().all()

            for item in items:
                results.append({
                    "id": item.id,
                    "category": item.category,
                    "title": item.title,
                    "content": item.content,
                    "summary": item.summary,
                    "tags": item.tags or []
                })
        except Exception as e:
            logger.warning(f"Vector knowledge search failed, falling back to text search: {e}")
            filters = [KnowledgeItem.visibility == visibility]
            if category:
                filters.append(KnowledgeItem.category == category)
            stmt = select(KnowledgeItem).where(and_(*filters)).limit(limit)
            exec_res = await self.db.execute(stmt)
            items = exec_res.scalars().all()
            for item in items:
                results.append({
                    "id": item.id,
                    "category": item.category,
                    "title": item.title,
                    "content": item.content,
                    "summary": item.summary,
                    "tags": item.tags or []
                })

        return results
