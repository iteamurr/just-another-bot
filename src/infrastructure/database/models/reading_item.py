from __future__ import annotations

from sqlalchemy import ARRAY, Column, DateTime, String, Text, func

from src.domain.reading.entities import ReadingItem
from src.domain.reading.value_objects import ReadingSource, SourceKind, Takeaway
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

    @classmethod
    def from_domain(cls, item: ReadingItem) -> ReadingItemModel:
        return cls(
            id=item.id,
            title=item.title,
            source_kind=item.source.kind.value,
            source_url=item.source.url,
            takeaway=item.takeaway.text,
            tags=item.tags,
            finished_at=item.finished_at,
            created_at=item.created_at,
        )

    def to_domain(self) -> ReadingItem:
        return ReadingItem(
            id=self.id,
            title=self.title,
            source=ReadingSource(kind=SourceKind(self.source_kind), url=self.source_url),
            takeaway=Takeaway(text=self.takeaway),
            tags=list(self.tags),
            finished_at=self.finished_at,  # type: ignore[arg-type]
            created_at=self.created_at,  # type: ignore[arg-type]
        )
