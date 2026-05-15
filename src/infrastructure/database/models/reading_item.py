from sqlalchemy import ARRAY, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models.base import Base


class ReadingItemModel(Base):
    __tablename__ = "reading_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    source_kind: Mapped[str] = mapped_column(String(20), nullable=False)
    source_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    takeaway: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String(100)), nullable=False, default=list)
    finished_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), nullable=False)
