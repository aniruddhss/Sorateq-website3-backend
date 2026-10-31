import datetime
import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    DateTime,
    Integer,
    Float,
    ForeignKey,
    Index,
    func
)
from sqlalchemy.dialects.postgresql import JSONB, ARRAY, TSVECTOR
from sqlalchemy.orm import relationship
from app.db.session import Base

try:
    from pgvector.sqlalchemy import Vector
except ImportError:
    from sqlalchemy.types import UserDefinedType

    class Vector(UserDefinedType):
        def __init__(self, dim=1536):
            self.dim = dim

        def get_col_spec(self, **kw):
            return f"vector({self.dim})"



class Project(Base):
    __tablename__ = "projects"

    id = Column(String(64), primary_key=True, default=lambda: f"proj_{uuid.uuid4().hex[:10]}")
    slug = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(256), nullable=False)
    tagline = Column(String(512), nullable=True)
    summary = Column(Text, nullable=False)
    full_description = Column(Text, nullable=True)
    industry = Column(String(128), nullable=False, index=True)
    project_type = Column(String(128), nullable=False, index=True)
    problem = Column(Text, nullable=True)
    solution = Column(Text, nullable=True)
    
    # Rich structured fields
    features = Column(JSONB, default=list)
    technologies = Column(JSONB, default=list)
    services = Column(JSONB, default=list)
    stage = Column(String(128), default="Production Live")
    project_outcome = Column(Text, nullable=True)
    proof = Column(Text, nullable=True)
    metrics = Column(JSONB, default=list)
    public_url = Column(String(512), nullable=True)
    image = Column(String(512), nullable=True)
    case_study = Column(Text, nullable=True)
    
    # Metadata & Vector
    featured = Column(Boolean, default=False)
    visibility = Column(String(32), default="PUBLIC", index=True)  # PUBLIC, INTERNAL, PRIVATE
    tags = Column(JSONB, default=list)
    keywords = Column(JSONB, default=list)
    
    # Vector embedding (1536 dimension for text-embedding-3-small)
    embedding = Column(Vector(1536), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("ix_projects_visibility_industry", "visibility", "industry"),
    )


class KnowledgeItem(Base):
    __tablename__ = "knowledge_items"

    id = Column(String(64), primary_key=True, default=lambda: f"know_{uuid.uuid4().hex[:10]}")
    category = Column(String(64), nullable=False, index=True)  # company, capabilities, methodology, technology, commercial, faqs
    title = Column(String(256), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    visibility = Column(String(32), default="PUBLIC", index=True)  # PUBLIC, INTERNAL, PRIVATE
    tags = Column(JSONB, default=list)
    metadata_json = Column(JSONB, default=dict)
    
    # Vector embedding
    embedding = Column(Vector(1536), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(String(64), primary_key=True)
    email = Column(String(256), nullable=True, index=True)
    email_valid = Column(Boolean, default=False)
    source = Column(String(128), default="landing")
    utm_params = Column(JSONB, default=dict)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_seen_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    conversations = relationship("Conversation", back_populates="visitor", cascade="all, delete-orphan")
    leads = relationship("Lead", back_populates="visitor", cascade="all, delete-orphan")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(64), primary_key=True, default=lambda: f"conv_{uuid.uuid4().hex[:12]}")
    visitor_id = Column(String(64), ForeignKey("visitors.id", ondelete="CASCADE"), nullable=False, index=True)
    visitor_email = Column(String(256), nullable=True)
    state = Column(String(64), default="NEW", index=True)  # NEW, INTRODUCTION, PROJECT_DISCOVERY, etc.
    summary = Column(Text, default="")
    project_profile = Column(JSONB, default=dict)  # structured extracted fields
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_message_at = Column(DateTime(timezone=True), server_default=func.now())

    visitor = relationship("Visitor", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")


class Message(Base):
    __tablename__ = "messages"

    id = Column(String(64), primary_key=True, default=lambda: f"msg_{uuid.uuid4().hex[:12]}")
    conversation_id = Column(String(64), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(32), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    intent = Column(String(64), nullable=True)
    confidence = Column(Integer, nullable=True)
    ui_blocks = Column(JSONB, default=list)
    tool_calls = Column(JSONB, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    conversation = relationship("Conversation", back_populates="messages")


class Lead(Base):
    __tablename__ = "leads"

    id = Column(String(64), primary_key=True, default=lambda: f"lead_{uuid.uuid4().hex[:10]}")
    visitor_id = Column(String(64), ForeignKey("visitors.id", ondelete="CASCADE"), nullable=False, index=True)
    email = Column(String(256), nullable=True, index=True)
    name = Column(String(256), nullable=True)
    company = Column(String(256), nullable=True)
    role = Column(String(128), nullable=True)
    
    # Project Profile Summary
    project_type = Column(String(128), nullable=True)
    industry = Column(String(128), nullable=True)
    stage = Column(String(64), nullable=True)
    budget = Column(String(64), nullable=True)
    timeline = Column(String(64), nullable=True)
    urgency = Column(String(64), nullable=True)
    
    qualification_state = Column(String(64), default="prospect")  # prospect, qualifying, qualified, unqualified, partner
    qualification_score = Column(Integer, default=0)
    meeting_state = Column(String(64), default="none")  # none, requested, scheduled, completed
    summary = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    visitor = relationship("Visitor", back_populates="leads")


class MeetingRequest(Base):
    __tablename__ = "meeting_requests"

    id = Column(String(64), primary_key=True, default=lambda: f"meet_{uuid.uuid4().hex[:10]}")
    visitor_id = Column(String(64), ForeignKey("visitors.id", ondelete="CASCADE"), nullable=False)
    email = Column(String(256), nullable=False)
    name = Column(String(256), nullable=True)
    preferred_date = Column(String(64), nullable=True)
    preferred_time_slot = Column(String(64), nullable=True)
    company = Column(String(256), nullable=True)
    conversation_id = Column(String(64), nullable=True, index=True)
    timezone = Column(String(64), default="UTC")
    notes = Column(Text, nullable=True)
    status = Column(String(32), default="PENDING")  # PENDING, CONFIRMED, CANCELLED
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class VisitorSession(Base):
    __tablename__ = "visitor_sessions"

    id = Column(String(64), primary_key=True)
    visitor_id = Column(String(64), ForeignKey("visitors.id", ondelete="CASCADE"), nullable=False, index=True)
    email = Column(String(256), nullable=False)
    active_conversation_id = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)


class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(String(64), primary_key=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String(64), nullable=True)
    visibility = Column(String(32), default="PUBLIC", index=True)
    tags = Column(JSONB, default=list)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


class Capability(Base):
    __tablename__ = "capabilities"

    id = Column(String(64), primary_key=True)
    slug = Column(String(128), unique=True, nullable=False)
    title = Column(String(256), nullable=False)
    short_description = Column(Text, nullable=True)
    full_description = Column(Text, nullable=True)
    deliverables = Column(JSONB, default=list)
    visibility = Column(String(32), default="PUBLIC", index=True)
    tags = Column(JSONB, default=list)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


class PromptVersion(Base):
    __tablename__ = "prompt_versions"

    id = Column(String(64), primary_key=True)
    version = Column(String(32), nullable=False)
    name = Column(String(256), nullable=False)
    system_prompt = Column(Text, nullable=False)
    is_active = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ContactRequest(Base):
    __tablename__ = "contact_requests"

    id = Column(String(64), primary_key=True)
    visitor_id = Column(String(64), ForeignKey("visitors.id", ondelete="SET NULL"), nullable=True, index=True)
    name = Column(String(256), nullable=True)
    email = Column(String(256), nullable=False)
    company = Column(String(256), nullable=True)
    message = Column(Text, nullable=True)
    payload = Column(JSONB, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id = Column(String(64), primary_key=True)
    event_type = Column(String(64), nullable=False, index=True)
    visitor_id = Column(String(64), nullable=True, index=True)
    session_id = Column(String(64), nullable=True)
    conversation_id = Column(String(64), nullable=True)
    metadata_json = Column(JSONB, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)


class ModelUsage(Base):
    __tablename__ = "model_usage"

    id = Column(String(64), primary_key=True)
    conversation_id = Column(String(64), nullable=True, index=True)
    model = Column(String(128), nullable=False)
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    estimated_cost_usd = Column(Float, default=0)
    request_type = Column(String(64), nullable=True)
    latency_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)