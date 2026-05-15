from sqlalchemy import ARRAY, Column, DateTime, String, Text, func

from src.infrastructure.database.models.base import Base


class ReadingItemModel(Base):
    __tablename__ = "reading_items"

    id = Column(String(36), primary_key=True, nullable=False)
    title = Column(String(500), nullable=False)
    source_kind = Column(String(20), nullable=False)
    source_url = Column(String(2048), nullable=True)
    takeaway = Column(Text, nullable=False)
    tags = Column(ARRAY(String(100)), nullable=False, server_default="{}")
    finished_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
