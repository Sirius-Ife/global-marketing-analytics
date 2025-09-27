-- models/marts/mkt_attribution_first_last.sql
with touches as (
  select
    t.touch_id,
    t.user_id,
    t.touch_time,
    t.channel,
    c.conversion_id,
    c.conversion_time,
    c.conversion_value,
    row_number() over(partition by c.conversion_id order by t.touch_time asc) as rn_first,
    row_number() over(partition by c.conversion_id order by t.touch_time desc) as rn_last
  from {{ ref('mkt_touchpoints') }} t
  join {{ ref('conversions') }} c
    on t.user_id = c.user_id
   and t.touch_time <= c.conversion_time
   and t.touch_time >= c.conversion_time - interval '30 days'  -- lookback window
)
, first_touch as (
  select conversion_id, channel, conversion_value
  from touches where rn_first = 1
)
, last_touch as (
  select conversion_id, channel, conversion_value
  from touches where rn_last = 1
)
select 'first_touch' as model, channel, sum(conversion_value) as revenue, count(*) as conversions
from first_touch
group by channel
union all
select 'last_touch' as model, channel, sum(conversion_value) as revenue, count(*) as conversions
from last_touch
group by channel
order by model, revenue desc;
