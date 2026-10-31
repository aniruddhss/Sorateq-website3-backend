"""
Backend store for the Next.js app. Replaces the local JSON store.

Payloads use camelCase to match the TypeScript types in src/lib/types.ts.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import (
    AnalyticsEvent,
    Capability,
    ContactRequest,
    Conversation,
    FAQ,
    KnowledgeItem,
    Lead,
    MeetingRequest,
    Project,
    Message,
    ModelUsage,
    PromptVersion,
    Visitor,
    VisitorSession,
)
from app.db.session import get_db

router = APIRouter(prefix="/appstore", tags=["App Store"])

SESSION_DAYS = 30


def iso(dt: Optional[datetime]) -> Optional[str]:
    return dt.astimezone(timezone.utc).isoformat() if dt else None


def now() -> datetime:
    return datetime.now(timezone.utc)


def new_id(prefix: str) -> str:
    import uuid

    return f"{prefix}_{uuid.uuid4().hex[:12]}"


# ---------- serializers ----------

def visitor_out(v: Visitor) -> dict[str, Any]:
    return {
        "id": v.id,
        "email": v.email or "",
        "emailValid": bool(v.email_valid),
        "createdAt": iso(v.created_at),
        "lastSeenAt": iso(v.last_seen_at),
        "source": v.source,
        "utmParams": v.utm_params or {},
        "userAgent": v.user_agent,
    }


def session_out(s: VisitorSession) -> dict[str, Any]:
    return {
        "sessionId": s.id,
        "visitorId": s.visitor_id,
        "email": s.email,
        "createdAt": iso(s.created_at),
        "expiresAt": iso(s.expires_at),
        "activeConversationId": s.active_conversation_id,
    }


def message_out(m: Message) -> dict[str, Any]:
    return {
        "id": m.id,
        "conversationId": m.conversation_id,
        "role": m.role,
        "content": m.content,
        "intent": m.intent,
        "confidence": m.confidence,
        "uiBlocks": m.ui_blocks or [],
        "toolCalls": m.tool_calls or [],
        "createdAt": iso(m.created_at),
    }


def conversation_out(c: Conversation, messages: list[Message]) -> dict[str, Any]:
    return {
        "id": c.id,
        "visitorId": c.visitor_id,
        "visitorEmail": c.visitor_email or "",
        "state": c.state,
        "summary": c.summary or "",
        "projectProfile": c.project_profile or {},
        "messages": [message_out(m) for m in messages],
        "createdAt": iso(c.created_at),
        "updatedAt": iso(c.updated_at),
        "lastMessageAt": iso(c.last_message_at),
    }


def lead_out(lead: Lead) -> dict[str, Any]:
    return {
        "id": lead.id,
        "visitorId": lead.visitor_id,
        "email": lead.email or "",
        "name": lead.name,
        "company": lead.company,
        "role": lead.role,
        "projectType": lead.project_type,
        "industry": lead.industry,
        "stage": lead.stage,
        "budget": lead.budget,
        "timeline": lead.timeline,
        "urgency": lead.urgency,
        "qualificationState": lead.qualification_state,
        "qualificationScore": lead.qualification_score or 0,
        "meetingState": lead.meeting_state,
        "summary": lead.summary,
        "createdAt": iso(lead.created_at),
        "updatedAt": iso(lead.updated_at),
    }


def faq_out(f: FAQ) -> dict[str, Any]:
    return {
        "id": f.id,
        "question": f.question,
        "answer": f.answer,
        "category": f.category,
        "visibility": f.visibility,
        "tags": f.tags or [],
    }


def capability_out(c: Capability) -> dict[str, Any]:
    return {
        "id": c.id,
        "slug": c.slug,
        "title": c.title,
        "shortDescription": c.short_description,
        "fullDescription": c.full_description,
        "deliverables": c.deliverables or [],
        "visibility": c.visibility,
        "tags": c.tags or [],
    }


def prompt_out(p: PromptVersion) -> dict[str, Any]:
    return {
        "id": p.id,
        "version": p.version,
        "name": p.name,
        "systemPrompt": p.system_prompt,
        "isActive": bool(p.is_active),
        "createdAt": iso(p.created_at),
    }


def meeting_out(m: MeetingRequest) -> dict[str, Any]:
    return {
        "id": m.id,
        "visitorId": m.visitor_id,
        "conversationId": m.conversation_id,
        "email": m.email,
        "name": m.name,
        "company": m.company,
        "preferredDate": m.preferred_date,
        "preferredTimeSlot": m.preferred_time_slot,
        "timezone": m.timezone,
        "notes": m.notes,
        "status": m.status,
        "createdAt": iso(m.created_at),
    }


def analytics_out(e: AnalyticsEvent) -> dict[str, Any]:
    return {
        "id": e.id,
        "eventType": e.event_type,
        "visitorId": e.visitor_id,
        "sessionId": e.session_id,
        "conversationId": e.conversation_id,
        "metadata": e.metadata_json or {},
        "timestamp": iso(e.created_at),
    }


def usage_out(u: ModelUsage) -> dict[str, Any]:
    return {
        "id": u.id,
        "conversationId": u.conversation_id,
        "model": u.model,
        "promptTokens": u.prompt_tokens or 0,
        "completionTokens": u.completion_tokens or 0,
        "totalTokens": u.total_tokens or 0,
        "estimatedCostUsd": u.estimated_cost_usd or 0,
        "requestType": u.request_type,
        "latencyMs": u.latency_ms,
        "timestamp": iso(u.created_at),
    }


# ---------- visitors & sessions ----------

class VisitorIn(BaseModel):
    email: str
    source: Optional[str] = None
    utmParams: Optional[dict[str, str]] = None
    userAgent: Optional[str] = None


@router.post("/visitors/get-or-create")
async def get_or_create_visitor(payload: VisitorIn, db: AsyncSession = Depends(get_db)):
    email = payload.email.lower().strip()
    result = await db.execute(select(Visitor).where(Visitor.email == email).limit(1))
    visitor = result.scalar_one_or_none()
    if visitor is None:
        visitor = Visitor(
            id=new_id("vis"),
            email=email,
            email_valid=True,
            source=payload.source or "landing",
            utm_params=payload.utmParams or {},
            user_agent=payload.userAgent,
        )
        db.add(visitor)
        await db.flush()
        await _ensure_lead(db, visitor.id, email)
    else:
        visitor.last_seen_at = now()
        if payload.source and not visitor.source:
            visitor.source = payload.source
        await db.flush()
    return visitor_out(visitor)


@router.get("/visitors/{visitor_id}")
async def get_visitor(visitor_id: str, db: AsyncSession = Depends(get_db)):
    visitor = await db.get(Visitor, visitor_id)
    if visitor is None:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return visitor_out(visitor)


class SessionIn(BaseModel):
    visitorId: str
    email: str


@router.post("/sessions")
async def create_session(payload: SessionIn, db: AsyncSession = Depends(get_db)):
    session = VisitorSession(
        id=new_id("sess"),
        visitor_id=payload.visitorId,
        email=payload.email.lower().strip(),
        expires_at=now() + timedelta(days=SESSION_DAYS),
    )
    db.add(session)
    await db.flush()
    return session_out(session)


@router.get("/sessions/{session_id}")
async def get_session(session_id: str, db: AsyncSession = Depends(get_db)):
    session = await db.get(VisitorSession, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.expires_at and session.expires_at < now():
        await db.delete(session)
        await db.flush()
        raise HTTPException(status_code=404, detail="Session expired")
    return session_out(session)


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str, db: AsyncSession = Depends(get_db)):
    session = await db.get(VisitorSession, session_id)
    if session is not None:
        await db.delete(session)
        await db.flush()
    return {"success": True}


# ---------- conversations & messages ----------

class ConversationIn(BaseModel):
    visitorId: str
    visitorEmail: str = ""


async def _latest_conversation(db: AsyncSession, visitor_id: str) -> Optional[Conversation]:
    result = await db.execute(
        select(Conversation)
        .where(Conversation.visitor_id == visitor_id)
        .order_by(Conversation.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


@router.post("/conversations/get-or-create")
async def get_or_create_conversation(payload: ConversationIn, db: AsyncSession = Depends(get_db)):
    conv = await _latest_conversation(db, payload.visitorId)
    if conv is None:
        conv = Conversation(
            id=new_id("conv"),
            visitor_id=payload.visitorId,
            visitor_email=payload.visitorEmail,
            state="NEW",
            summary="",
            project_profile={},
        )
        db.add(conv)
        await db.flush()
    return conversation_out(conv, [])


@router.post("/conversations")
async def create_conversation(payload: ConversationIn, db: AsyncSession = Depends(get_db)):
    conv = Conversation(
        id=new_id("conv"),
        visitor_id=payload.visitorId,
        visitor_email=payload.visitorEmail,
        state="NEW",
        summary="",
        project_profile={},
    )
    db.add(conv)
    await db.flush()
    return conversation_out(conv, [])


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str, db: AsyncSession = Depends(get_db)):
    conv = await db.get(Conversation, conversation_id)
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    result = await db.execute(
        select(Message).where(Message.conversation_id == conv.id).order_by(Message.created_at)
    )
    return conversation_out(conv, list(result.scalars().all()))


class ConversationUpdate(BaseModel):
    state: Optional[str] = None
    summary: Optional[str] = None
    projectProfile: Optional[dict[str, Any]] = None


@router.patch("/conversations/{conversation_id}")
async def update_conversation(conversation_id: str, payload: ConversationUpdate, db: AsyncSession = Depends(get_db)):
    conv = await db.get(Conversation, conversation_id)
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if payload.state is not None:
        conv.state = payload.state
    if payload.summary is not None:
        conv.summary = payload.summary
    if payload.projectProfile is not None:
        conv.project_profile = payload.projectProfile
    await db.flush()
    return {"success": True}


class MessageIn(BaseModel):
    role: str
    content: str
    intent: Optional[str] = None
    confidence: Optional[int] = None
    uiBlocks: list[Any] = Field(default_factory=list)
    toolCalls: list[Any] = Field(default_factory=list)


@router.post("/conversations/{conversation_id}/messages")
async def add_message(conversation_id: str, payload: MessageIn, db: AsyncSession = Depends(get_db)):
    conv = await db.get(Conversation, conversation_id)
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    msg = Message(
        id=new_id("msg"),
        conversation_id=conversation_id,
        role=payload.role,
        content=payload.content,
        intent=payload.intent,
        confidence=payload.confidence,
        ui_blocks=payload.uiBlocks,
        tool_calls=payload.toolCalls,
    )
    db.add(msg)
    stamp = now()
    conv.last_message_at = stamp
    conv.updated_at = stamp
    await db.flush()
    return message_out(msg)


@router.get("/conversations")
async def list_conversations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Conversation).order_by(Conversation.created_at.desc()))
    return [conversation_out(c, []) for c in result.scalars().all()]


# ---------- leads & meetings ----------

async def _ensure_lead(db: AsyncSession, visitor_id: str, email: str) -> Lead:
    result = await db.execute(
        select(Lead).where((Lead.visitor_id == visitor_id) | (Lead.email == email)).limit(1)
    )
    lead = result.scalar_one_or_none()
    if lead is None:
        lead = Lead(
            id=new_id("lead"),
            visitor_id=visitor_id,
            email=email,
            qualification_state="prospect",
            qualification_score=20,
            meeting_state="none",
        )
        db.add(lead)
        await db.flush()
    return lead


class LeadEnsureIn(BaseModel):
    visitorId: str
    email: str


@router.post("/leads/ensure")
async def ensure_lead(payload: LeadEnsureIn, db: AsyncSession = Depends(get_db)):
    lead = await _ensure_lead(db, payload.visitorId, payload.email.lower())
    return lead_out(lead)


class LeadUpdate(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    role: Optional[str] = None
    projectType: Optional[str] = None
    industry: Optional[str] = None
    stage: Optional[str] = None
    budget: Optional[str] = None
    timeline: Optional[str] = None
    urgency: Optional[str] = None
    qualificationState: Optional[str] = None
    qualificationScore: Optional[int] = None
    meetingState: Optional[str] = None
    summary: Optional[str] = None


FIELD_MAP = {
    "name": "name",
    "company": "company",
    "role": "role",
    "projectType": "project_type",
    "industry": "industry",
    "stage": "stage",
    "budget": "budget",
    "timeline": "timeline",
    "urgency": "urgency",
    "qualificationState": "qualification_state",
    "qualificationScore": "qualification_score",
    "meetingState": "meeting_state",
    "summary": "summary",
}


@router.patch("/leads/{lead_id}")
async def update_lead(lead_id: str, payload: LeadUpdate, db: AsyncSession = Depends(get_db)):
    lead = await db.get(Lead, lead_id)
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    for api_name, column in FIELD_MAP.items():
        value = getattr(payload, api_name)
        if value is not None:
            setattr(lead, column, value)
    await db.flush()
    return lead_out(lead)


@router.get("/leads")
async def list_leads(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lead).order_by(Lead.created_at.desc()))
    return [lead_out(l) for l in result.scalars().all()]


class MeetingIn(BaseModel):
    visitorId: str
    email: str
    name: Optional[str] = None
    company: Optional[str] = None
    conversationId: Optional[str] = None
    scheduledTime: Optional[str] = None
    preferredDate: Optional[str] = None
    preferredTimeSlot: Optional[str] = None
    timezone: str = "UTC"
    notes: Optional[str] = None


@router.post("/meetings")
async def create_meeting(payload: MeetingIn, db: AsyncSession = Depends(get_db)):
    meeting = MeetingRequest(
        id=new_id("meet"),
        visitor_id=payload.visitorId,
        email=payload.email,
        name=payload.name,
        company=payload.company,
        conversation_id=payload.conversationId,
        preferred_date=payload.preferredDate or payload.scheduledTime,
        preferred_time_slot=payload.preferredTimeSlot,
        timezone=payload.timezone,
        notes=payload.notes,
        status="PENDING",
    )
    db.add(meeting)
    await db.flush()
    return meeting_out(meeting)


@router.get("/meetings")
async def list_meetings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MeetingRequest).order_by(MeetingRequest.created_at.desc()))
    return [meeting_out(m) for m in result.scalars().all()]


# ---------- contact requests ----------

class ContactIn(BaseModel):
    visitorId: Optional[str] = None
    name: Optional[str] = None
    email: str
    company: Optional[str] = None
    message: Optional[str] = None
    payload: dict[str, Any] = Field(default_factory=dict)


@router.post("/contact-requests")
async def create_contact_request(payload: ContactIn, db: AsyncSession = Depends(get_db)):
    req = ContactRequest(
        id=new_id("contact"),
        visitor_id=payload.visitorId,
        name=payload.name,
        email=payload.email.lower().strip(),
        company=payload.company,
        message=payload.message,
        payload=payload.payload,
    )
    db.add(req)
    await db.flush()
    return {"id": req.id, "createdAt": iso(req.created_at)}


# ---------- analytics & model usage ----------

class AnalyticsIn(BaseModel):
    eventType: str
    visitorId: Optional[str] = None
    sessionId: Optional[str] = None
    conversationId: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


@router.post("/analytics")
async def track_analytics(payload: AnalyticsIn, db: AsyncSession = Depends(get_db)):
    event = AnalyticsEvent(
        id=new_id("evt"),
        event_type=payload.eventType,
        visitor_id=payload.visitorId,
        session_id=payload.sessionId,
        conversation_id=payload.conversationId,
        metadata_json=payload.metadata,
    )
    db.add(event)
    await db.flush()
    return analytics_out(event)


@router.get("/analytics")
async def list_analytics(limit: int = Query(200, le=1000), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AnalyticsEvent).order_by(AnalyticsEvent.created_at.desc()).limit(limit))
    return [analytics_out(e) for e in result.scalars().all()]


class ModelUsageIn(BaseModel):
    conversationId: Optional[str] = None
    model: str
    promptTokens: int = 0
    completionTokens: int = 0
    totalTokens: int = 0
    estimatedCostUsd: float = 0
    requestType: Optional[str] = None
    latencyMs: Optional[int] = None


@router.post("/model-usage")
async def record_model_usage(payload: ModelUsageIn, db: AsyncSession = Depends(get_db)):
    usage = ModelUsage(
        id=new_id("use"),
        conversation_id=payload.conversationId,
        model=payload.model,
        prompt_tokens=payload.promptTokens,
        completion_tokens=payload.completionTokens,
        total_tokens=payload.totalTokens,
        estimated_cost_usd=payload.estimatedCostUsd,
        request_type=payload.requestType,
        latency_ms=payload.latencyMs,
    )
    db.add(usage)
    await db.flush()
    return usage_out(usage)


@router.get("/model-usage")
async def list_model_usage(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ModelUsage).order_by(ModelUsage.created_at.desc()))
    return [usage_out(u) for u in result.scalars().all()]


# ---------- content: faqs, capabilities, prompts ----------

@router.get("/faqs")
async def list_faqs(visibility: str = "PUBLIC", db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FAQ).where(FAQ.visibility.in_(_visible(visibility))))
    return [faq_out(f) for f in result.scalars().all()]


@router.get("/capabilities")
async def list_capabilities(visibility: str = "PUBLIC", db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Capability).where(Capability.visibility.in_(_visible(visibility))))
    return [capability_out(c) for c in result.scalars().all()]


@router.get("/prompts/active")
async def active_prompt(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PromptVersion).where(PromptVersion.is_active.is_(True)).limit(1))
    prompt = result.scalar_one_or_none()
    if prompt is None:
        raise HTTPException(status_code=404, detail="No active prompt")
    return prompt_out(prompt)


def _visible(level: str) -> list[str]:
    # INTERNAL includes PUBLIC; PRIVATE is never served over the API.
    return ["PUBLIC", "INTERNAL"] if level == "INTERNAL" else ["PUBLIC"]


# ---------- projects, knowledge, methodology (read) ----------

def project_out(p: Project) -> dict[str, Any]:
    return {
        "id": p.id,
        "slug": p.slug,
        "name": p.name,
        "tagline": p.tagline or "",
        "summary": p.summary,
        "fullDescription": p.full_description or "",
        "industry": p.industry,
        "projectType": p.project_type,
        "problem": p.problem or "",
        "solution": p.solution or "",
        "features": p.features or [],
        "technologies": p.technologies or [],
        "services": p.services or [],
        "stage": p.stage or "",
        "projectOutcome": p.project_outcome or "",
        "proof": p.proof,
        "metrics": p.metrics or [],
        "publicUrl": p.public_url,
        "image": p.image,
        "heroImage": p.image,
        "galleryImages": [p.image] if p.image else [],
        "images": [p.image] if p.image else [],
        "caseStudyContent": p.case_study,
        "featured": bool(p.featured),
        "visibility": p.visibility or "PUBLIC",
        "tags": p.tags or [],
        "keywords": p.keywords or [],
        "updatedAt": iso(p.updated_at),
    }


@router.get("/projects")
async def list_projects(visibility: str = "PUBLIC", db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).where(Project.visibility.in_(_visible(visibility))))
    return [project_out(p) for p in result.scalars().all()]


@router.get("/projects/search")
async def search_projects(
    q: str = "",
    industry: Optional[str] = None,
    type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Project).where(Project.visibility == "PUBLIC")
    if industry:
        stmt = stmt.where(Project.industry.ilike(f"%{industry}%"))
    if type:
        stmt = stmt.where(Project.project_type.ilike(f"%{type}%"))
    result = await db.execute(stmt)
    needle = q.strip().lower()
    projects = [project_out(p) for p in result.scalars().all()]
    if needle:
        projects = [
            p for p in projects
            if needle in " ".join(
                [p["name"], p["tagline"], p["summary"], p["industry"], " ".join(p["tags"]), " ".join(p["keywords"])]
            ).lower()
        ]
    return projects


@router.get("/projects/{slug}")
async def get_project(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).where(Project.slug == slug, Project.visibility == "PUBLIC"))
    project = result.scalar_one_or_none()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_out(project)


@router.get("/knowledge")
async def list_knowledge(visibility: str = "PUBLIC", db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(KnowledgeItem).where(KnowledgeItem.visibility.in_(_visible(visibility))))
    return [
        {
            "id": k.id,
            "title": k.title,
            "category": k.category,
            "content": k.content,
            "visibility": k.visibility,
            "tags": k.tags or [],
            "updatedAt": iso(k.updated_at),
        }
        for k in result.scalars().all()
    ]

@router.get("/methodology")
async def list_methodology(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(KnowledgeItem).where(KnowledgeItem.category == "methodology")
    )
    steps = []
    for k in result.scalars().all():
        meta = k.metadata_json or {}
        steps.append({
            "step": meta.get("step", 0),
            "title": k.title,
            "subtitle": meta.get("subtitle", ""),
            "description": meta.get("description", ""),
            "deliverables": meta.get("deliverables", []),
            "duration": meta.get("duration", ""),
        })
    return sorted(steps, key=lambda s: s["step"])

@router.get("/prompts")
async def list_prompts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PromptVersion).order_by(PromptVersion.created_at.desc()))
    return [prompt_out(p) for p in result.scalars().all()]

# ---------- admin writes (mirror the Next.js admin actions) ----------

class ProjectUpsert(BaseModel):
    id: Optional[str] = None
    slug: str
    name: str
    tagline: Optional[str] = ""
    summary: str = ""
    fullDescription: Optional[str] = ""
    industry: str = ""
    projectType: str = ""
    problem: Optional[str] = ""
    solution: Optional[str] = ""
    features: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)
    services: list[str] = Field(default_factory=list)
    stage: Optional[str] = ""
    projectOutcome: Optional[str] = ""
    proof: Optional[str] = None
    metrics: list[dict[str, str]] = Field(default_factory=list)
    publicUrl: Optional[str] = None
    image: Optional[str] = None
    heroImage: Optional[str] = None
    caseStudyContent: Optional[str] = None
    featured: bool = False
    visibility: str = "PUBLIC"
    tags: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)


@router.put("/admin/projects")
async def admin_upsert_project(payload: ProjectUpsert, db: AsyncSession = Depends(get_db)):
    existing = None
    if payload.id:
        existing = await db.get(Project, payload.id)
    if existing is None:
        existing = (await db.execute(select(Project).where(Project.slug == payload.slug))).scalar_one_or_none()
    project = existing or Project(id=payload.id or new_id("proj"))
    project.slug = payload.slug
    project.name = payload.name
    project.tagline = payload.tagline
    project.summary = payload.summary
    project.full_description = payload.fullDescription
    project.industry = payload.industry
    project.project_type = payload.projectType
    project.problem = payload.problem
    project.solution = payload.solution
    project.features = payload.features
    project.technologies = payload.technologies
    project.services = payload.services
    project.stage = payload.stage
    project.project_outcome = payload.projectOutcome
    project.proof = payload.proof
    project.metrics = payload.metrics
    project.public_url = payload.publicUrl
    project.image = payload.image or payload.heroImage
    project.case_study = payload.caseStudyContent
    project.featured = payload.featured
    project.visibility = payload.visibility
    project.tags = payload.tags
    project.keywords = payload.keywords
    db.add(project)
    await db.flush()
    return project_out(project)


@router.delete("/admin/projects/{project_id}")
async def admin_delete_project(project_id: str, db: AsyncSession = Depends(get_db)):
    project = await db.get(Project, project_id)
    if project is None:
        return {"success": False}
    await db.delete(project)
    await db.flush()
    return {"success": True}


class FAQUpsert(BaseModel):
    id: str
    question: str
    answer: str
    category: Optional[str] = None
    visibility: str = "PUBLIC"
    tags: list[str] = Field(default_factory=list)


@router.put("/admin/faqs")
async def admin_upsert_faq(payload: FAQUpsert, db: AsyncSession = Depends(get_db)):
    faq = await db.get(FAQ, payload.id) or FAQ(id=payload.id)
    faq.question = payload.question
    faq.answer = payload.answer
    faq.category = payload.category
    faq.visibility = payload.visibility
    faq.tags = payload.tags
    db.add(faq)
    await db.flush()
    return faq_out(faq)


@router.delete("/admin/faqs/{faq_id}")
async def admin_delete_faq(faq_id: str, db: AsyncSession = Depends(get_db)):
    faq = await db.get(FAQ, faq_id)
    if faq is None:
        return {"success": False}
    await db.delete(faq)
    await db.flush()
    return {"success": True}


class CapabilityUpsert(BaseModel):
    id: str
    slug: str
    title: str
    shortDescription: Optional[str] = None
    fullDescription: Optional[str] = None
    deliverables: list[str] = Field(default_factory=list)
    visibility: str = "PUBLIC"
    tags: list[str] = Field(default_factory=list)


@router.put("/admin/capabilities")
async def admin_upsert_capability(payload: CapabilityUpsert, db: AsyncSession = Depends(get_db)):
    cap = await db.get(Capability, payload.id) or Capability(id=payload.id)
    cap.slug = payload.slug
    cap.title = payload.title
    cap.short_description = payload.shortDescription
    cap.full_description = payload.fullDescription
    cap.deliverables = payload.deliverables
    cap.visibility = payload.visibility
    cap.tags = payload.tags
    db.add(cap)
    await db.flush()
    return capability_out(cap)


class KnowledgeUpsert(BaseModel):
    id: str
    title: str
    category: str
    content: str
    visibility: str = "PUBLIC"
    tags: list[str] = Field(default_factory=list)


@router.put("/admin/knowledge")
async def admin_upsert_knowledge(payload: KnowledgeUpsert, db: AsyncSession = Depends(get_db)):
    item = await db.get(KnowledgeItem, payload.id) or KnowledgeItem(id=payload.id)
    item.title = payload.title
    item.category = payload.category
    item.content = payload.content
    item.summary = payload.content[:300]
    item.visibility = payload.visibility
    item.tags = payload.tags
    db.add(item)
    await db.flush()
    return {"id": item.id, "title": item.title, "category": item.category, "content": item.content,
            "visibility": item.visibility, "tags": item.tags or []}


class PromptUpsert(BaseModel):
    id: str
    version: str
    name: str
    systemPrompt: str
    isActive: bool = False


@router.put("/admin/prompts")
async def admin_upsert_prompt(payload: PromptUpsert, db: AsyncSession = Depends(get_db)):
    # Only one prompt may be active at a time, matching the store's behaviour.
    if payload.isActive:
        await db.execute(update(PromptVersion).values(is_active=False))
    prompt = await db.get(PromptVersion, payload.id) or PromptVersion(id=payload.id)
    prompt.version = payload.version
    prompt.name = payload.name
    prompt.system_prompt = payload.systemPrompt
    prompt.is_active = payload.isActive
    db.add(prompt)
    await db.flush()
    return prompt_out(prompt)


class LeadPatch(BaseModel):
    id: str
    updates: dict[str, Any] = Field(default_factory=dict)


@router.patch("/admin/leads")
async def admin_update_lead(payload: LeadPatch, db: AsyncSession = Depends(get_db)):
    lead = await db.get(Lead, payload.id)
    if lead is None:
        return {"success": False}
    for api_name, column in FIELD_MAP.items():
        if api_name in payload.updates and payload.updates[api_name] is not None:
            setattr(lead, column, payload.updates[api_name])
    await db.flush()
    return lead_out(lead)

@router.get("/contact-requests")
async def list_contact_requests(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ContactRequest).order_by(ContactRequest.created_at.desc()))
    return [
        {
            "id": c.id,
            "visitorId": c.visitor_id,
            "name": c.name,
            "email": c.email,
            "company": c.company,
            "message": c.message,
            "payload": c.payload or {},
            "createdAt": iso(c.created_at),
        }
        for c in result.scalars().all()
    ]
