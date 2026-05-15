"""Начальная миграция — три таблицы

Revision ID: 0001
Revises:
Create Date: 2026-05-15
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: str | None = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "reading_items",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("source_kind", sa.String(20), nullable=False),
        sa.Column("source_url", sa.String(2048), nullable=True),
        sa.Column("takeaway", sa.Text, nullable=False),
        sa.Column("tags", postgresql.ARRAY(sa.String(100)), nullable=False, server_default="{}"),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "review_cards",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("item_id", sa.String(36), nullable=False, index=True),
        sa.Column("ease_factor", sa.Float, nullable=False),
        sa.Column("interval_days", sa.Integer, nullable=False),
        sa.Column("repetitions", sa.Integer, nullable=False),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column("cached_question", sa.Text, nullable=True),
    )

    op.create_table(
        "review_history",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("card_id", sa.String(36), nullable=False, index=True),
        sa.Column("grade", sa.Integer, nullable=False),
        sa.Column("ease_factor_after", sa.Float, nullable=False),
        sa.Column("interval_days_after", sa.Integer, nullable=False),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("review_history")
    op.drop_table("review_cards")
    op.drop_table("reading_items")
