-- models/staging/stg_web_events.sql
with raw as (
  select * from {{ source('raw','web_events') }} -- or ref('raw_web_events') if seeded
)
select
  event_id,
  user_id,
  (event_time)::timestamp as event_time,
  event_type,
  page,
  utm_source,
  utm_medium,
  utm_campaign,
  cost::numeric as cost
from raw
