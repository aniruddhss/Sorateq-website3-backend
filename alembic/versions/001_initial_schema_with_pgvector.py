"""initial_schema_with_pgvector

Revision ID: 001_initial
Revises: 
Create Date: 2026-10-03 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
import pgvector

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Enable pgvector extension
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # 2. Projects Table
    op.create_table(
        'projects',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('slug', sa.String(128), nullable=False, unique=True),
        sa.Column('name', sa.String(256), nullable=False),
        sa.Column('tagline', sa.String(512), nullable=True),
        sa.Column('summary', sa.Text(), nullable=False),
        sa.Column('full_description', sa.Text(), nullable=True),
        sa.Column('industry', sa.String(128), nullable=False),
        sa.Column('project_type', sa.String(128), nullable=False),
        sa.Column('problem', sa.Text(), nullable=True),
        sa.Column('solution', sa.Text(), nullable=True),
        sa.Column('features', JSONB, server_default='[]'),
        sa.Column('technologies', JSONB, server_default='[]'),
        sa.Column('services', JSONB, server_default='[]'),
        sa.Column('stage', sa.String(128), server_default='Production Live'),
        sa.Column('project_outcome', sa.Text(), nullable=True),
        sa.Column('proof', sa.Text(), nullable=True),
        sa.Column('metrics', JSONB, server_default='[]'),
        sa.Column('public_url', sa.String(512), nullable=True),
        sa.Column('case_study', sa.Text(), nullable=True),
        sa.Column('featured', sa.Boolean(), server_default='false'),
        sa.Column('visibility', sa.String(32), server_default='PUBLIC'),
        sa.Column('tags', JSONB, server_default='[]'),
        sa.Column('keywords', JSONB, server_default='[]'),
        sa.Column('embedding', pgvector.sqlalchemy.Vector(1536), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('ix_projects_slug', 'projects', ['slug'])
    op.create_index('ix_projects_visibility', 'projects', ['visibility'])
    op.create_index('ix_projects_industry', 'projects', ['industry'])

    # 3. Knowledge Items Table
    op.create_table(
        'knowledge_items',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('category', sa.String(64), nullable=False),
        sa.Column('title', sa.String(256), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('visibility', sa.String(32), server_default='PUBLIC'),
        sa.Column('tags', JSONB, server_default='[]'),
        sa.Column('metadata_json', JSONB, server_default='{}'),
        sa.Column('embedding', pgvector.sqlalchemy.Vector(1536), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('ix_knowledge_category', 'knowledge_items', ['category'])
    op.create_index('ix_knowledge_visibility', 'knowledge_items', ['visibility'])

    # 4. Visitors Table
    op.create_table(
        'visitors',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('email', sa.String(256), nullable=True),
        sa.Column('email_valid', sa.Boolean(), server_default='false'),
        sa.Column('source', sa.String(128), server_default='landing'),
        sa.Column('utm_params', JSONB, server_default='{}'),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('last_seen_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('ix_visitors_email', 'visitors', ['email'])

    # 5. Conversations Table
    op.create_table(
        'conversations',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('visitor_id', sa.String(64), sa.ForeignKey('visitors.id', ondelete='CASCADE'), nullable=False),
        sa.Column('visitor_email', sa.String(256), nullable=True),
        sa.Column('state', sa.String(64), server_default='NEW'),
        sa.Column('summary', sa.Text(), server_default=''),
        sa.Column('project_profile', JSONB, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('last_message_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('ix_conversations_visitor_id', 'conversations', ['visitor_id'])
    op.create_index('ix_conversations_state', 'conversations', ['state'])

    # 6. Messages Table
    op.create_table(
        'messages',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('conversation_id', sa.String(64), sa.ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(32), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('intent', sa.String(64), nullable=True),
        sa.Column('confidence', sa.Integer(), nullable=True),
        sa.Column('ui_blocks', JSONB, server_default='[]'),
        sa.Column('tool_calls', JSONB, server_default='[]'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('ix_messages_conversation_id', 'messages', ['conversation_id'])

    # 7. Leads Table
    op.create_table(
        'leads',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('visitor_id', sa.String(64), sa.ForeignKey('visitors.id', ondelete='CASCADE'), nullable=False),
        sa.Column('email', sa.String(256), nullable=True),
        sa.Column('name', sa.String(256), nullable=True),
        sa.Column('company', sa.String(256), nullable=True),
        sa.Column('role', sa.String(128), nullable=True),
        sa.Column('project_type', sa.String(128), nullable=True),
        sa.Column('industry', sa.String(128), nullable=True),
        sa.Column('stage', sa.String(64), nullable=True),
        sa.Column('budget', sa.String(64), nullable=True),
        sa.Column('timeline', sa.String(64), nullable=True),
        sa.Column('urgency', sa.String(64), nullable=True),
        sa.Column('qualification_state', sa.String(64), server_default='prospect'),
        sa.Column('qualification_score', sa.Integer(), server_default='0'),
        sa.Column('meeting_state', sa.String(64), server_default='none'),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('ix_leads_visitor_id', 'leads', ['visitor_id'])
    op.create_index('ix_leads_email', 'leads', ['email'])

    # 8. Meeting Requests Table
    op.create_table(
        'meeting_requests',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('visitor_id', sa.String(64), sa.ForeignKey('visitors.id', ondelete='CASCADE'), nullable=False),
        sa.Column('email', sa.String(256), nullable=False),
        sa.Column('name', sa.String(256), nullable=True),
        sa.Column('preferred_date', sa.String(64), nullable=True),
        sa.Column('preferred_time_slot', sa.String(64), nullable=True),
        sa.Column('timezone', sa.String(64), server_default='UTC'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('status', sa.String(32), server_default='PENDING'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )


def downgrade() -> None:
    op.drop_table('meeting_requests')
    op.drop_table('leads')
    op.drop_table('messages')
    op.drop_table('conversations')
    op.drop_table('visitors')
    op.drop_table('knowledge_items')
    op.drop_table('projects')
    op.execute("DROP EXTENSION IF EXISTS vector;")
