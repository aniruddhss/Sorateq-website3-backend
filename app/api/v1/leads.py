from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.models import Lead, MeetingRequest

router = APIRouter(prefix="/leads", tags=["Leads & Meetings"])


@router.post("")
async def capture_lead(
    payload: dict,
    db: AsyncSession = Depends(get_db)
):
    """
    Captures or updates qualified lead information.
    """
    lead = Lead(
        visitor_id=payload.get("visitor_id", "anonymous"),
        email=payload.get("email"),
        name=payload.get("name"),
        company=payload.get("company"),
        role=payload.get("role"),
        project_type=payload.get("project_type"),
        industry=payload.get("industry"),
        stage=payload.get("stage"),
        budget=payload.get("budget"),
        timeline=payload.get("timeline"),
        urgency=payload.get("urgency"),
        qualification_state="qualifying",
        qualification_score=50,
        summary=payload.get("summary")
    )
    db.add(lead)
    await db.commit()
    return {"status": "success", "lead_id": lead.id}


@router.post("/meetings")
async def schedule_meeting(
    payload: dict,
    db: AsyncSession = Depends(get_db)
):
    """
    Creates a new meeting discovery booking request.
    """
    meeting = MeetingRequest(
        visitor_id=payload.get("visitor_id", "anonymous"),
        email=payload.get("email", "unknown@client.com"),
        name=payload.get("name", ""),
        preferred_date=payload.get("preferred_date"),
        preferred_time_slot=payload.get("preferred_time_slot"),
        timezone=payload.get("timezone", "UTC"),
        notes=payload.get("notes", "")
    )
    db.add(meeting)
    await db.commit()
    return {"status": "success", "meeting_id": meeting.id, "message": "Meeting request logged."}
