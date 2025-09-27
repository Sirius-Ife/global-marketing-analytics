with g as (
  select date, sum(cost) as cost, 'google' as channel from {{ ref('stg_google_ads') }} group by date
),
ln as (
  select date, sum(cost) as cost, 'linkedin' as channel from {{ ref('stg_linkedin') }} group by date
),
em as (
  select send_date::date as date, sum(0) as cost, 'email' as channel from {{ ref('stg_email') }} group by send_date
),
web as (
  select date_trunc('day', event_time)::date as date, sum(cost) as cost, coalesce(utm_source,'direct') as channel
  from {{ ref('stg_web_events') }}
  group by 1,3
)
select * from g
union all
select * from ln
union all
select * from em
union all
select * from web
