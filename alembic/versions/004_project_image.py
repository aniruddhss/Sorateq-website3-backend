"""project cover image

Revision ID: 004_project_image
Revises: 003_meeting_fields
Create Date: 2026-10-28 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = "004_project_image"
down_revision = "003_meeting_fields"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("projects", sa.Column("image", sa.String(512), nullable=True))


def downgrade() -> None:
    op.drop_column("projects", "image")
