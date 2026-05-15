-- name: insert_review_history_entry!
INSERT INTO review_history (id, card_id, grade, ease_factor_after, interval_days_after, reviewed_at)
VALUES (:id, :card_id, :grade, :ease_factor_after, :interval_days_after, :reviewed_at);

-- name: get_review_history_by_card
SELECT *
FROM review_history
WHERE card_id = :card_id
ORDER BY reviewed_at DESC;
