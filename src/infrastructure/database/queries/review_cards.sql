-- name: get_review_card_by_id^
SELECT *
FROM review_cards
WHERE id = :card_id;

-- name: get_review_card_by_item_id^
SELECT *
FROM review_cards
WHERE item_id = :item_id;

-- name: insert_review_card!
INSERT INTO review_cards (id, item_id, ease_factor, interval_days, repetitions, due_at, cached_question)
VALUES (:id, :item_id, :ease_factor, :interval_days, :repetitions, :due_at, :cached_question);

-- name: update_review_card!
UPDATE review_cards
SET ease_factor      = :ease_factor,
    interval_days    = :interval_days,
    repetitions      = :repetitions,
    due_at           = :due_at,
    cached_question  = :cached_question
WHERE id = :id;

-- name: count_due_review_cards$
SELECT COUNT(*)
FROM review_cards
WHERE due_at <= :now;

-- name: retention_stats^
SELECT
    ROUND(
        AVG(CASE WHEN grade >= 3 THEN 1.0 ELSE 0.0 END)::numeric, 4
    )                          AS overall_retention,
    ROUND(AVG(ease_factor_after)::numeric, 4) AS avg_ease_factor,
    COUNT(*)                   AS total_reviews
FROM review_history;
