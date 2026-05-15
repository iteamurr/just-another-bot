from src.domain.review.entities import ReviewHistoryEntry
from src.infrastructure.database.models.review_history import ReviewHistoryModel


def model_to_review_history_entry(model: ReviewHistoryModel) -> ReviewHistoryEntry:
    return ReviewHistoryEntry(
        id=model.id,
        card_id=model.card_id,
        grade=model.grade,
        ease_factor_after=model.ease_factor_after,
        interval_days_after=model.interval_days_after,
        reviewed_at=model.reviewed_at,  # type: ignore[arg-type]
    )


def review_history_entry_to_model(entry: ReviewHistoryEntry) -> ReviewHistoryModel:
    return ReviewHistoryModel(
        id=entry.id,
        card_id=entry.card_id,
        grade=entry.grade,
        ease_factor_after=entry.ease_factor_after,
        interval_days_after=entry.interval_days_after,
        reviewed_at=entry.reviewed_at,
    )
