# 📊 SQL Queries for Marketing Analytics

This document contains example SQL queries that power the metrics and dashboards defined in [`dashboards/wireframes.md`](../dashboards/wireframes.md).  
All queries assume the existence of staging tables created via dbt (`stg_*`) that clean and unify raw source data.

---

## 1. Funnel Analysis

Tracks user progression through the marketing funnel: **Sessions → MQLs → SQLs → Opportunities → Wins**.

```sql
with funnel as (
    select
        user_id,
        min(case when event = 'session' then event_time end) as first_session,
        min(case when event = 'mql' then event_time end) as first_mql,
        min(case when event = 'sql' then event_time end) as first_sql,
        min(case when event = 'opportunity' then event_time end) as first_opportunity,
        min(case when event = 'won' then event_time end) as first_win
    from stg_crm_events
    group by user_id
)
select
    count(distinct user_id) as total_users,
    count(distinct case when first_session is not null then user_id end) as sessions,
    count(distinct case when first_mql is not null then user_id end) as mqls,
    count(distinct case when first_sql is not null then user_id end) as sqls,
    count(distinct case when first_opportunity is not null then user_id end) as opportunities,
    count(distinct case when first_win is not null then user_id end) as wins
from funnel;
