-- models/marts/mkt_touchpoints.sql
select
  event_id as touch_id,
  user_id,
  event_time as touch_time,
  coalesce(utm_source, 'direct') as channel,
  cost as touch_cost
from {{ ref('stg_web_events') }}
where event_type in ('click','page_view')
