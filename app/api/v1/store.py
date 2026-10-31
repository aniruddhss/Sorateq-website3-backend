"""
Persistence endpoints used by the Next.js app in place of its JSON store.

Shapes mirror the Next.js store (camelCase in, camelCase out) so the app can
switch over route by route. Writes are idempotent where an ID is supplied.
"""

from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Conversation, Lead, MeetingRequest, Message, Visitor
from app.db.session import get_db

router = APIRouter(prefix="/store", tags=["Store"])


def _iso(dt: Optional[datetime]) -> Optional[str]:
    return dt.astimezone(timezone.utc).isoformat() if dt else None


class VisitorIn(BaseModel):
    id: str
    email: Optional[str] = None
    emailValid: bool = False
    source: str = "landing"
    utmParams: dict[str, Any] = Field(default_factory=dict)
    userAgent: Optional[str] = None


def _visitor_out(v: Visitor) -> dict[str, Any]:
    return {
        "id": v.id,
        "email": v.email,
        "emailValid": v.email_valid,
        "source": v.source,
        "utmParams": v.utm_params or {},
        "userAgent": v.user_agent,
        "createdAt": _iso(v.created_at),
        "lastSeenAt": _iso(v.last_seen_at),
    }


@router.put("/visitors")
async def upsert_visitor(payload: VisitorIn, db: AsyncSession = Depends(get_db)):
    visitor = await db.get(Visitor, payload.id)
    if visitor is None:
        visitor = Visitor(id=payload.id)
        db.add(visitor)
    visitor.email = payload.email
    visitor.email_valid = payload.emailValid
    visitor.source = payload.source
    visitor.utm_params = payload.utmParams
    visitor.user_agent = payload.userAgent
    await db.flush()
    return _visitor_out(visitor)


@router.get("/visitors/{visitor_id}")
async def get_visitor(visitor_id: str, db: AsyncSession = Depends(get_db)):
    visitor = await db.get(Visitor, visitor_id)
    if visitor is None:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return _visitor_out(visitor)


class ConversationIn(BaseModel):
    id: Optional[str] = None
    visitorId: str
    visitorEmail: Optional[str] = None
    state: str = "NEW"
    summary: str = ""
    projectProfile: dict[str, Any] = Field(default_factory=dict)


def _conversation_out(c: Conversation, messages: list[Message]) -> dict[str, Any]:
    return {
        "id": c.id,
        "visitorId": c.visitor_id,
        "visitorEmail": c.visitor_email,
        "state": c.state,
        "summary": c.summary or "",
        "projectProfile": c.project_profile or {},
        "messages": [_message_out(m) for m in messages],
        "createdAt": _iso(c.created_at),
        "updatedAt": _iso(c.updated_at),
        "lastMessageAt": _iso(c.last_message_at),
    }


@router.post("/conversations")
async def create_conversation(payload: ConversationIn, db: AsyncSession = Depends(get_db)):
    conv = Conversation(
        visitor_id=payload.visitorId,
        visitor_email=payload.visitorEmail,
        state=payload.state,
        summary=payload.summary,
        project_profile=payload.projectProfile,
    )
    if payload.id:
        conv.id = payload.id
    db.add(conv)
    await db.flush()
    return _conversation_out(conv, [])


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str, db: AsyncSession = Depends(get_db)):
    conv = await db.get(Conversation, conversation_id)
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    result = await db.execute(
        select(Message).where(Message.conversation_id == conv.id).order_by(Message.created_at)
    )
    return _conversation_out(conv, list(result.scalars().all()))


@router.get("/visitors/{visitor_id}/conversations")
async def list_visitor_conversations(visitor_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Conversation).where(Conversation.visitor_id == visitor_id).order_by(Conversation.created_at)
    )
    return [_conversation_out(c, []) for c in result.scalars().all()]


class MessageIn(BaseModel):
    id: Optional[str] = None
    role: str
    content: str
    intent: Optional[str] = None
    confidence: Optional[int] = None
    uiBlocks: list[Any] = Field(default_factory=list)
    toolCalls: list[Any] = Field(default_factory=list)


def _message_out(m: Message) -> dict[str, Any]:
    return {
        "id": m.id,
        "role": m.role,
        "content": m.content,
        "intent": m.intent,
        "confidence": m.confidence,
        "uiBlocks": m.ui_blocks or [],
        "toolCalls": m.tool_calls or [],
        "createdAt": _iso(m.created_at),
    }


@router.post("/conversations/{conversation_id}/messages")
async def add_message(conversation_id: str, payload: MessageIn, db: AsyncSession = Depends(get_db)):
    conv = await db.get(Conversation, conversation_id)
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    msg = Message(
        conversation_id=conversation_id,
        role=payload.role,
        content=payload.content,
        intent=payload.intent,
        confidence=payload.confidence,
        ui_blocks=payload.uiBlocks,
        tool_calls=payload.toolCalls,
    )
    if payload.id:
        msg.id = payload.id
    db.add(msg)
    conv.last_message_at = datetime.now(timezone.utc)
    await db.flush()
    return _message_out(msg)


class LeadIn(BaseModel):
    id: Optional[str] = None
    visitorId: str
    email: Optional[str] = None
    name: Optional[str] = None
    company: Optional[str] = None
    role: Optional[str] = None
    projectType: Optional[str] = None
    industry: Optional[str] = None
    stage: Optional[str] = None
    budget: Optional[str] = None
    timeline: Optional[str] = None
    urgency: Optional[str] = None
    qualificationState: str = "prospect"
    qualificationScore: int = 0
    meetingState: str = "none"
    summary: Optional[str] = None


def _lead_out(lead: Lead) -> dict[str, Any]:
    return {
        "id": lead.id,
        "visitorId": lead.visitor_id,
        "email": lead.email,
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
        "qualificationScore": lead.qualification_score,
        "meetingState": lead.meeting_state,
        "summary": lead.summary,
        "createdAt": _iso(lead.created_at),
        "updatedAt": _iso(lead.updated_at),
    }


@router.put("/leads")
async def upsert_lead(payload: LeadIn, db: AsyncSession = Depends(get_db)):
    lead = await db.get(Lead, payload.id) if payload.id else None
    if lead is None:
        lead = Lead(visitor_id=payload.visitorId)
        if payload.id:
            lead.id = payload.id
        db.add(lead)
    lead.visitor_id = payload.visitorId
    lead.email = payload.email
    lead.name = payload.name
    lead.company = payload.company
    lead.role = payload.role
    lead.project_type = payload.projectType
    lead.industry = payload.industry
    lead.stage = payload.stage
    lead.budget = payload.budget
    lead.timeline = payload.timeline
    lead.urgency = payload.urgency
    lead.qualification_state = payload.qualificationState
    lead.qualification_score = payload.qualificationScore
    lead.meeting_state = payload.meetingState
    lead.summary = payload.summary
    await db.flush()
    return _lead_out(lead)


@router.get("/leads")
async def list_leads(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lead).order_by(Lead.created_at.desc()))
    return [_lead_out(l) for l in result.scalars().all()]


class MeetingIn(BaseModel):
    id: Optional[str] = None
    visitorId: str
    email: str
    name: Optional[str] = None
    preferredDate: Optional[str] = None
    preferredTimeSlot: Optional[str] = None
    timezone: str = "UTC"
    notes: Optional[str] = None
    status: str = "PENDING"


@router.post("/meetings")
async def create_meeting(payload: MeetingIn, db: AsyncSession = Depends(get_db)):
    meeting = MeetingRequest(
        visitor_id=payload.visitorId,
        email=payload.email,
        name=payload.name,
        preferred_date=payload.preferredDate,
        preferred_time_slot=payload.preferredTimeSlot,
        timezone=payload.timezone,
        notes=payload.notes,
        status=payload.status,
    )
    if payload.id:
        meeting.id = payload.id
    db.add(meeting)
    await db.flush()
    return {
        "id": meeting.id,
        "visitorId": meeting.visitor_id,
        "email": meeting.email,
        "name": meeting.name,
        "preferredDate": meeting.preferred_date,
        "preferredTimeSlot": meeting.preferred_time_slot,
        "timezone": meeting.timezone,
        "notes": meeting.notes,
        "status": meeting.status,
        "createdAt": _iso(meeting.created_at),
    }


@router.get("/meetings")
async def list_meetings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MeetingRequest).order_by(MeetingRequest.created_at.desc()))
    return [
        {
            "id": m.id,
            "visitorId": m.visitor_id,
            "email": m.email,
            "name": m.name,
            "preferredDate": m.preferred_date,
            "preferredTimeSlot": m.preferred_time_slot,
            "timezone": m.timezone,
            "notes": m.notes,
            "status": m.status,
            "createdAt": _iso(m.created_at),
        }
        for m in result.scalars().all()
    ]
