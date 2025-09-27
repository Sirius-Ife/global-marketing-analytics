-- models/marts/mkt_attribution_linear.sql
with touches as (
  select
    t.touch_id,
    t.user_id,
    t.touch_time,
    t.channel,
    c.conversion_id,
    c.conversion_time,
    c.conversion_value
  from {{ ref('mkt_touchpoints') }} t
  join {{ ref('conversions') }} c
    on t.user_id = c.user_id
   and t.touch_time <= c.conversion_time
   and t.touch_time >= c.conversion_time - interval '30 days'
),
counts as (
  select conversion_id, count(1) as touch_count
  from touches
  group by conversion_id
),
attributed as (
  select
    t.conversion_id,
    t.channel,
    (c.conversion_value::numeric / cnt.touch_count) as attributed_value
  from touches t
  join counts cnt using (conversion_id)
  join {{ ref('conversions') }} c using (conversion_id)
)
select channel, sum(attributed_value) as revenue, count(distinct conversion_id) as conversions
from attributed
group by channel
order by revenue desc;
