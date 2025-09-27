# Global Marketing Analytics (demo)
Simulates a global marketing analytics pipeline: ingestion from Ads/Email/Web/CRM → dbt transformations → attribution models → BI dashboard.

## Quickstart (dev)
1. `docker-compose up -d` (start Postgres)
2. `pip install -r requirements.txt`
3. `python scripts/generate_mock_data.py`
4. `python scripts/load_data.py`
5. `cd dbt_project && dbt run && dbt test`
6. Connect Looker Studio / Metabase to `postgres://...` and build the dashboard using provided queries.