-- models/marts/conversions.sql
select
  event_id as conversion_id,
  user_id,
  event_time as conversion_time,
  coalesce((nullif(event_properties->>'revenue', '') )::numeric, 0) as conversion_value
from {{ ref('stg_web_events') }}
where event_type = 'conversion'
union all
select
  lead_id as conversion_id,
  user_id,
  created_at::timestamp as conversion_time,
  revenue::numeric as conversion_value
from {{ ref('stg_crm_leads') }}
where coalesce(revenue::numeric,0) > 0
