KPI cards (top row)

Total Spend (period) — SELECT sum(cost) FROM mkt_spend WHERE date BETWEEN ...

Total Revenue (period) — SELECT sum(revenue) FROM conversions WHERE conversion_time BETWEEN ...

ROAS — total_revenue / NULLIF(total_spend,0)

CAC — sum(spend)/count(distinct new_customers) (define new_customers as first conversion in a period)

Time series

Spend by channel (line chart) — SELECT date, channel, sum(cost) FROM mkt_spend GROUP BY 1,2

Revenue by channel (line) from attribution table.

Attribution comparison (table)

Table showing channel / conversions / revenue for first_touch, last_touch, linear. Use mkt_attribution_first_last and mkt_attribution_linear.