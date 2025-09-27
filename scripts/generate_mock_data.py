# scripts/generate_mock_data.py
# pip install faker pandas numpy

import csv
import random
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd
import numpy as np

fake = Faker()
random.seed(42)
Faker.seed(42)

NUM_USERS = 300
START = datetime(2024, 8, 1)
END = datetime(2024, 9, 30)
channels = ['google','linkedin','email','organic','direct']

# generate user ids
users = [f"user_{i:04d}" for i in range(1, NUM_USERS+1)]

def daterange(start, end):
    for n in range(int((end - start).days) + 1):
        yield start + timedelta(n)

# 1) web_events
events = []
for user in users:
    # each user gets 1-8 sessions
    sessions = random.randint(1, 8)
    base = START + timedelta(days=random.randint(0, (END-START).days))
    for s in range(sessions):
        t = base + timedelta(days=random.randint(0, (END-START).days), hours=random.randint(0,23), minutes=random.randint(0,59))
        channel = random.choices(channels, weights=[0.35,0.15,0.2,0.2,0.1])[0]
        # some events are clicks, some page views, some conversions
        events.append({
            "event_id": fake.uuid4(),
            "user_id": user,
            "event_time": t.isoformat(),
            "event_type": random.choices(['page_view','click','conversion'], weights=[70,25,5])[0],
            "page": random.choice(['/','/pricing','/signup','/checkout']),
            "utm_source": channel if channel not in ['organic','direct'] else None,
            "utm_medium": 'cpc' if channel in ['google','linkedin'] else ('email' if channel=='email' else None),
            "utm_campaign": random.choice(['Hire-Intl','Retention','Brand-Awareness']),
            "cost": round(random.random() * (3.0 if channel in ['google','linkedin'] else 0.0), 2)
        })

events_df = pd.DataFrame(events)
events_df.to_csv("data/seeds/web_events.csv", index=False)

# 2) google_ads / linkedin simplified daily aggregates
ads = []
for campaign in ['Hire-Intl','Retention','Brand-Awareness']:
    for d in daterange(START, END):
        ads.append({
            "date": d.date().isoformat(),
            "campaign_name": campaign,
            "clicks": random.randint(0, 200),
            "impressions": random.randint(100, 10000),
            "cost": round(random.random()*200, 2),
            "conversions": random.randint(0, 5),
            "conversion_value": round(random.random()*1000, 2)
        })
pd.DataFrame(ads).to_csv("data/seeds/google_ads.csv", index=False)
pd.DataFrame(ads).sample(frac=0.5).to_csv("data/seeds/linkedin_ads.csv", index=False)

# 3) emails
emails = []
for c in ['Onboarding','Promo','News']:
    for d in daterange(START, END):
        sends = random.randint(50, 300)
        opens = int(sends * random.uniform(0.1, 0.35))
        clicks = int(opens * random.uniform(0.1, 0.3))
        conv = int(clicks * random.uniform(0.02, 0.2))
        emails.append({
            "send_date": d.date().isoformat(),
            "campaign_name": c,
            "sends": sends,
            "opens": opens,
            "clicks": clicks,
            "conversions": conv,
            "conversion_value": round(conv * random.uniform(50,300),2)
        })
pd.DataFrame(emails).to_csv("data/seeds/email_campaigns.csv", index=False)

# 4) crm leads (derive some leads from conversions)
leads = []
conv_events = events_df[events_df['event_type'] == 'conversion'].sample(frac=0.8)
for idx,row in conv_events.iterrows():
    revenue = round(random.uniform(100,1000),2)
    leads.append({
        "lead_id": fake.uuid4(),
        "user_id": row['user_id'],
        "created_at": row['event_time'],
        "lead_stage": random.choice(['MQL','SQL','Opportunity','Won']),
        "stage_updated_at": (pd.to_datetime(row['event_time']) + pd.Timedelta(days=random.randint(1,14))).isoformat(),
        "assigned_segment": random.choice(['SMB','Mid-Market','Enterprise']),
        "first_touch_channel": row['utm_source'] if row['utm_source'] else 'direct',
        "first_touch_time": row['event_time'],
        "revenue": revenue if random.random() < 0.25 else 0.0
    })
pd.DataFrame(leads).to_csv("data/seeds/crm_leads.csv", index=False)

print("Mock data generated in data/seeds/")
