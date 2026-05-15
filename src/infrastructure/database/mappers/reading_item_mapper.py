from src.domain.reading.entities import ReadingItem
from src.domain.reading.value_objects import ReadingSource, SourceKind, Takeaway
from src.infrastructure.database.models.reading_item import ReadingItemModel


def model_to_reading_item(model: ReadingItemModel) -> ReadingItem:
    return ReadingItem(
        id=model.id,
        title=model.title,
        source=ReadingSource(kind=SourceKind(model.source_kind), url=model.source_url),
        takeaway=Takeaway(text=model.takeaway),
        tags=list(model.tags),
        finished_at=model.finished_at,  # type: ignore[arg-type]
        created_at=model.created_at,  # type: ignore[arg-type]
    )


def reading_item_to_model(item: ReadingItem) -> ReadingItemModel:
    return ReadingItemModel(
        id=item.id,
        title=item.title,
        source_kind=item.source.kind.value,
        source_url=item.source.url,
        takeaway=item.takeaway.text,
        tags=item.tags,
        finished_at=item.finished_at,
        created_at=item.created_at,
    )
