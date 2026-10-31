from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    conversation_id: Optional[str] = None
    visitor_id: Optional[str] = None
    visitor_email: Optional[str] = None
    message: str = Field(..., min_length=1)
    context_state: Optional[str] = None
    history: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    current_profile: Optional[Dict[str, Any]] = Field(default_factory=dict)
    question_count: Optional[int] = 0


class ProjectProfile(BaseModel):
    project_name: Optional[str] = None
    problem_statement: Optional[str] = None
    solution: Optional[str] = None
    industry: Optional[str] = None
    project_category: Optional[str] = None
    target_audience: Optional[str] = None
    users: Optional[str] = None
    current_stage: Optional[str] = None
    existing_product: Optional[str] = None
    mvp_requirements: Optional[List[str]] = None
    advanced_requirements: Optional[List[str]] = None
    platform: Optional[str] = None
    integrations: Optional[List[str]] = None
    ai_requirements: Optional[str] = None
    technical_constraints: Optional[str] = None
    preferred_technologies: Optional[List[str]] = None
    timeline: Optional[str] = None
    budget: Optional[str] = None
    business_model: Optional[str] = None
    urgency: Optional[str] = None
    decision_maker_status: Optional[str] = None
    meeting_intent: Optional[str] = None


class UIBlock(BaseModel):
    type: str  # text, project_card, project_grid, brief, tech_chips, meeting_card
    data: Dict[str, Any]


class ChatMessageResponse(BaseModel):
    conversation_id: str
    message_id: str
    role: str = "assistant"
    content: str
    intent: Optional[str] = None
    state: str
    project_profile: Optional[Dict[str, Any]] = None
    ui_blocks: List[UIBlock] = []
    created_at: str
