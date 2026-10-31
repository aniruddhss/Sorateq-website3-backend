"""app store tables: sessions, faqs, capabilities, prompts, contact requests, analytics, model usage

Revision ID: 002_app_store
Revises: 001_initial
Create Date: 2026-10-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = "002_app_store"
down_revision = "001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "visitor_sessions",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("visitor_id", sa.String(64), sa.ForeignKey("visitors.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("email", sa.String(256), nullable=False),
        sa.Column("active_conversation_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False, index=True),
    )

    op.create_table(
        "faqs",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("question", sa.Text, nullable=False),
        sa.Column("answer", sa.Text, nullable=False),
        sa.Column("category", sa.String(64), nullable=True),
        sa.Column("visibility", sa.String(32), server_default="PUBLIC", index=True),
        sa.Column("tags", JSONB, server_default="[]"),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "capabilities",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("slug", sa.String(128), unique=True, nullable=False),
        sa.Column("title", sa.String(256), nullable=False),
        sa.Column("short_description", sa.Text, nullable=True),
        sa.Column("full_description", sa.Text, nullable=True),
        sa.Column("deliverables", JSONB, server_default="[]"),
        sa.Column("visibility", sa.String(32), server_default="PUBLIC", index=True),
        sa.Column("tags", JSONB, server_default="[]"),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "prompt_versions",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("version", sa.String(32), nullable=False),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column("system_prompt", sa.Text, nullable=False),
        sa.Column("is_active", sa.Boolean, server_default=sa.text("false"), index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "contact_requests",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("visitor_id", sa.String(64), sa.ForeignKey("visitors.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("name", sa.String(256), nullable=True),
        sa.Column("email", sa.String(256), nullable=False),
        sa.Column("company", sa.String(256), nullable=True),
        sa.Column("message", sa.Text, nullable=True),
        sa.Column("payload", JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "analytics_events",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("event_type", sa.String(64), nullable=False, index=True),
        sa.Column("visitor_id", sa.String(64), nullable=True, index=True),
        sa.Column("session_id", sa.String(64), nullable=True),
        sa.Column("conversation_id", sa.String(64), nullable=True),
        sa.Column("metadata_json", JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), index=True),
    )

    op.create_table(
        "model_usage",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("conversation_id", sa.String(64), nullable=True, index=True),
        sa.Column("model", sa.String(128), nullable=False),
        sa.Column("prompt_tokens", sa.Integer, server_default="0"),
        sa.Column("completion_tokens", sa.Integer, server_default="0"),
        sa.Column("total_tokens", sa.Integer, server_default="0"),
        sa.Column("estimated_cost_usd", sa.Float, server_default="0"),
        sa.Column("request_type", sa.String(64), nullable=True),
        sa.Column("latency_ms", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), index=True),
    )

def downgrade() -> None:
    for table in ["model_usage", "analytics_events", "contact_requests", "prompt_versions", "capabilities", "faqs", "visitor_sessions"]:
        op.drop_table(table)
