select
  campaign_name,
  (date)::date as date,
  clicks::int,
  impressions::int,
  cost::numeric,
  conversions::int,
  conversion_value::numeric
from {{ ref('raw_google_ads') }}
