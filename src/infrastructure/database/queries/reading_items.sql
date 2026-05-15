-- name: get_reading_item_by_id^
SELECT *
FROM reading_items
WHERE id = :item_id;

-- name: insert_reading_item!
INSERT INTO reading_items (id, title, source_kind, source_url, takeaway, tags, finished_at, created_at)
VALUES (:id, :title, :source_kind, :source_url, :takeaway, :tags, :finished_at, :created_at);

-- name: update_reading_item!
UPDATE reading_items
SET title      = :title,
    source_kind = :source_kind,
    source_url  = :source_url,
    takeaway   = :takeaway,
    tags       = :tags,
    finished_at = :finished_at
WHERE id = :id;

-- name: count_reading_items$
SELECT COUNT(*) FROM reading_items;

-- name: count_reading_items_by_week
SELECT date_trunc('week', created_at) AS week,
       COUNT(*)::int                  AS count
FROM reading_items
WHERE created_at >= now() - interval '12 weeks'
GROUP BY 1
ORDER BY 1;

-- name: count_reading_items_by_tag
SELECT tag, COUNT(*)::int AS count
FROM reading_items,
     unnest(tags) AS tag
GROUP BY tag
ORDER BY count DESC;
