# scripts/load_data.py
# pip install sqlalchemy psycopg2-binary pandas

import os
from sqlalchemy import create_engine, text
import pandas as pd

DB_USER = os.getenv("DB_USER","postgres")
DB_PASS = os.getenv("DB_PASS","postgres")
DB_HOST = os.getenv("DB_HOST","localhost")
DB_PORT = os.getenv("DB_PORT","5432")
DB_NAME = os.getenv("DB_NAME","marketing")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}", future=True)

def load_csv_to_table(path, table_name):
    df = pd.read_csv(path)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"loaded {path} -> {table_name} ({len(df)} rows)")

if __name__ == "__main__":
    seeds = {
        "data/seeds/google_ads.csv": "raw_google_ads",
        "data/seeds/linkedin_ads.csv": "raw_linkedin_ads",
        "data/seeds/email_campaigns.csv": "raw_email_campaigns",
        "data/seeds/web_events.csv": "raw_web_events",
        "data/seeds/crm_leads.csv": "raw_crm_leads",
    }
    for p,t in seeds.items():
        load_csv_to_table(p,t)