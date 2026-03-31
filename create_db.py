import sqlite3
import pandas as pd
import numpy as np
import os

def create_sample_database():
    db_path = os.path.join(os.path.dirname(__file__), "sample_bi.db")
    conn = sqlite3.connect(db_path)

    np.random.seed(42)

    # --- Sales table ---
    regions = ["North", "South", "East", "West"]
    products = ["Analytics Pro", "Dashboard Lite", "DataSync", "ReportBuilder", "InsightAI"]
    channels = ["Direct", "Partner", "Online"]
    months = pd.date_range("2023-01-01", periods=24, freq="MS")

    sales_rows = []
    for month in months:
        for region in regions:
            for product in products:
                channel = np.random.choice(channels)
                revenue = np.random.randint(50000, 500000)
                units = np.random.randint(10, 300)
                cost = revenue * np.random.uniform(0.4, 0.65)
                sales_rows.append({
                    "date": month.strftime("%Y-%m-%d"),
                    "region": region,
                    "product": product,
                    "channel": channel,
                    "revenue": round(revenue, 2),
                    "units_sold": units,
                    "cost": round(cost, 2),
                    "profit": round(revenue - cost, 2),
                })
    df_sales = pd.DataFrame(sales_rows)
    df_sales.to_sql("sales", conn, if_exists="replace", index=False)

    # --- Users table ---
    plans = ["Free", "Starter", "Pro", "Enterprise"]
    user_rows = []
    for i in range(1, 501):
        signup = pd.Timestamp("2022-01-01") + pd.Timedelta(days=np.random.randint(0, 730))
        plan = np.random.choice(plans, p=[0.4, 0.3, 0.2, 0.1])
        mrr = {"Free": 0, "Starter": 29, "Pro": 99, "Enterprise": 499}[plan]
        user_rows.append({
            "user_id": i,
            "signup_date": signup.strftime("%Y-%m-%d"),
            "plan": plan,
            "region": np.random.choice(regions),
            "monthly_active_days": np.random.randint(0, 30),
            "mrr": mrr,
            "churned": int(np.random.random() < 0.15),
        })
    df_users = pd.DataFrame(user_rows)
    df_users.to_sql("users", conn, if_exists="replace", index=False)

    # --- Marketing table ---
    campaigns = ["Q1 Launch", "Summer Push", "Product Hunt", "SEO Organic", "Paid Social", "Email Drip"]
    mkt_rows = []
    for month in months:
        for campaign in campaigns:
            spend = np.random.randint(2000, 30000)
            leads = np.random.randint(20, 400)
            conversions = int(leads * np.random.uniform(0.05, 0.25))
            mkt_rows.append({
                "date": month.strftime("%Y-%m-%d"),
                "campaign": campaign,
                "channel": np.random.choice(["Paid", "Organic", "Email"]),
                "spend": round(spend, 2),
                "leads": leads,
                "conversions": conversions,
                "cac": round(spend / max(conversions, 1), 2),
            })
    df_mkt = pd.DataFrame(mkt_rows)
    df_mkt.to_sql("marketing", conn, if_exists="replace", index=False)

    conn.close()
    print(f"Database created at: {db_path}")
    return db_path

if __name__ == "__main__":
    create_sample_database()
