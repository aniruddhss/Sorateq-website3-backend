"""meeting company and conversation link

Revision ID: 003_meeting_fields
Revises: 002_app_store
Create Date: 2026-10-27 01:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = "003_meeting_fields"
down_revision = "002_app_store"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("meeting_requests", sa.Column("company", sa.String(256), nullable=True))
    op.add_column("meeting_requests", sa.Column("conversation_id", sa.String(64), nullable=True, index=True))


def downgrade() -> None:
    op.drop_column("meeting_requests", "conversation_id")
    op.drop_column("meeting_requests", "company")
