from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class KnowledgeItemSchema(BaseModel):
    id: str
    category: str
    title: str
    content: str
    summary: Optional[str] = None
    visibility: str = "PUBLIC"
    tags: List[str] = []
    metadata_json: Dict[str, Any] = {}


class KnowledgeQuery(BaseModel):
    query: str
    category: Optional[str] = None
    visibility: str = "PUBLIC"
    limit: int = 5
