from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class MetricItem(BaseModel):
    label: str
    value: str


class ProjectSchema(BaseModel):
    id: str
    slug: str
    name: str
    tagline: Optional[str] = None
    summary: str
    full_description: Optional[str] = None
    industry: str
    project_type: str
    problem: Optional[str] = None
    solution: Optional[str] = None
    features: List[str] = []
    technologies: List[str] = []
    services: List[str] = []
    stage: Optional[str] = "Production Live"
    project_outcome: Optional[str] = None
    proof: Optional[str] = None
    metrics: List[MetricItem] = []
    public_url: Optional[str] = None
    case_study: Optional[str] = None
    featured: bool = False
    visibility: str = "PUBLIC"
    tags: List[str] = []
    keywords: List[str] = []
    created_at: Optional[str] = None


class ProjectFilter(BaseModel):
    query: Optional[str] = None
    industry: Optional[str] = None
    technology: Optional[str] = None
    category: Optional[str] = None
    limit: int = 10
