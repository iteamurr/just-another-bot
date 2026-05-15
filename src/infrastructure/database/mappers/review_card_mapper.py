from src.domain.review.entities import ReviewCard
from src.domain.review.value_objects import EaseFactor
from src.infrastructure.database.models.review_card import ReviewCardModel


def model_to_review_card(model: ReviewCardModel) -> ReviewCard:
    return ReviewCard(
        id=model.id,
        item_id=model.item_id,
        ease_factor=EaseFactor(value=model.ease_factor),
        interval_days=model.interval_days,
        repetitions=model.repetitions,
        due_at=model.due_at,  # type: ignore[arg-type]
        cached_question=model.cached_question,
    )


def review_card_to_model(card: ReviewCard) -> ReviewCardModel:
    return ReviewCardModel(
        id=card.id,
        item_id=card.item_id,
        ease_factor=card.ease_factor.value,
        interval_days=card.interval_days,
        repetitions=card.repetitions,
        due_at=card.due_at,
        cached_question=card.cached_question,
    )
