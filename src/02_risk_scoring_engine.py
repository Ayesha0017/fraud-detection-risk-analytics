#!/usr/bin/env python3
"""
Production Script: Risk Scoring Matrix Heuristics & User Profiling
Filename: 02_risk_scoring_engine.py
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np

def main():
    # -------------------------------------------------------------------------
    # 1. Environment Routing & Workspace Setup
    # -------------------------------------------------------------------------
    BASE_DIR = Path(__file__).resolve().parent if "__file__" in locals() else Path(os.getcwd()).resolve().parent
    DATA_PROCESSED = BASE_DIR / "data" / "processed"

    # Load file tracking points from prior step
    staging_input = DATA_PROCESSED / "stg_master_prepared.parquet"
    if not staging_input.exists():
        print(f"[CRITICAL] Upstream tracking file not found: {staging_input}. Execute Step 1 script first.")
        return

    df = pd.read_parquet(staging_input)

    # -------------------------------------------------------------------------
    # 2. Temporal & Geographic Engineering Layer
    # -------------------------------------------------------------------------
    df["is_weekend"] = df["day_of_week"].isin([0, 6]).astype(int)
    df["is_night_transaction"] = df["hour"].between(1, 5).astype(int)
    df["high_distance_flag"] = (df["distance_from_home"] > 50).astype(int)

    # Arrange arrays chronologically to compute transaction window interval deltas
    df = df.sort_values(["customer_id", "transaction_time"])
    df["prev_transaction_time"] = df.groupby("customer_id")["transaction_time"].shift(1)

    time_delta = df["transaction_time"] - df["prev_transaction_time"]
    df["minutes_since_last_txn"] = (time_delta.dt.total_seconds() / 60.0).fillna(99999)
    df["rapid_txn_flag"] = (df["minutes_since_last_txn"] < 10).astype(int)

    # Map footprint diversity criteria
    df["merchant_diversity"] = df["customer_id"].map(df.groupby("customer_id")["merchant"].nunique())
    df["location_diversity"] = df["customer_id"].map(df.groupby("customer_id")["location"].nunique())

    # -------------------------------------------------------------------------
    # 3. Categorical Risk Metric Mapping Blocks
    # -------------------------------------------------------------------------
    merchant_risk_map = {
        "Cryptocurrency": 100, "Travel": 75, "Electronics": 75, "Gaming": 75,
        "Shopping Mall": 50, "Education": 50, "Healthcare": 50,
        "Restaurant": 25, "Entertainment": 25, "Groceries": 25, "Fuel": 25, "Food Delivery": 25
    }

    channel_risk_map = {
        "NetBanking": 100, "Card": 40, "UPI": 35
    }

    df["merchant_risk"] = df["merchant"].map(merchant_risk_map).fillna(25)
    df["channel_risk"] = df["channel"].map(channel_risk_map).fillna(35)

    df["amount_risk"] = pd.cut(
        df["amount"], 
        bins=[-float('inf'), 20000, 50000, 100000, 150000, float('inf')], 
        labels=[10, 30, 60, 80, 100]
    ).astype(int)

    df["distance_risk"] = pd.cut(
        df["distance_from_home"], 
        bins=[-float('inf'), 5, 10, 20, 50, float('inf')], 
        labels=[10, 30, 60, 80, 100]
    ).astype(int)

    df["time_risk"] = pd.cut(
        df["hour"], 
        bins=[-float('inf'), 5, 8, 22, float('inf')], 
        labels=[100, 50, 20, 40]
    ).astype(int)

    # -------------------------------------------------------------------------
    # 4. Scoring Calculations & Risk Segmentation
    # -------------------------------------------------------------------------
 
    df["risk_score"] = (
          0.30 * df["merchant_risk"]
        + 0.25 * df["amount_risk"]
        + 0.20 * df["distance_risk"]
        + 0.15 * df["channel_risk"]
        + 0.10 * df["time_risk"]
    )

    df["risk_segment"] = pd.cut(
        df["risk_score"],
        bins=[-float('inf'), 25, 50, 75, float('inf')],
        labels=["Low Risk", "Medium Risk", "High Risk", "Critical Risk"]
    ).astype(str)

    # -------------------------------------------------------------------------
    # 5. Production Exports Serialization
    # -------------------------------------------------------------------------
    profiles_output = DATA_PROCESSED / "customer_risk_segments.csv"
    features_output = DATA_PROCESSED / "stg_features_calculated.parquet"

    customer_profiles = df[["customer_id", "risk_score", "risk_segment"]].drop_duplicates()
    customer_profiles.to_csv(profiles_output, index=False)

    df.to_parquet(features_output, index=False)
    
    print(f"Stage 2 finalized {features_output}")

if __name__ == "__main__":
    main()