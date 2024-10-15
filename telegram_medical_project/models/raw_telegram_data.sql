-- models/ethio_medical.sql
{{ config(materialized='table') }}  -- Correcting the materialization syntax

WITH source_data AS (
    SELECT * 
    FROM {{ source('public', 'cleaned_telegram_data') }}  -- Use DBT's source function
)

SELECT
    channel_title,
    lower(channel_username) AS channel_username,
    message_id,
    message_text,
    message_date,
    media_path
     
   
      
FROM source_data
WHERE "message_text" IS NOT NULL