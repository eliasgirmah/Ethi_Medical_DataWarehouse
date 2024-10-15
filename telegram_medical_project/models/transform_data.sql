-- models/transform_data.sql
{{ config(materialized='table') }}

WITH cleaned_data AS (
    SELECT
        message_id,
        message_text,
        message_date, -- Assuming message_date is already a timestamp or date
        media_path
    FROM {{ ref('raw_telegram_data') }}
)

-- Transform data: Merge message_text columns and clean further
SELECT
    message_id,
    message_date, -- No need to use TO_TIMESTAMP if it's already in a timestamp format
    COALESCE(message_text, 'No Text Available') AS final_message_text, -- Handle missing message_text
    media_path,
    CASE
        WHEN media_path IS NOT NULL THEN TRUE
        ELSE FALSE
    END AS has_media
FROM cleaned_data
WHERE message_text IS NOT NULL
