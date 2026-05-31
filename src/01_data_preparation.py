#!/usr/bin/env python3
"""
Production Script: Data Ingestion and Baseline Preparation Pipeline
Filename: 01_data_preparation.py
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np

def main():
    # -------------------------------------------------------------------------
    # 1. Environment Routing & Workspace Setup
    # -------------------------------------------------------------------------
    print("[INFO] Initializing workspace directory streams...")
    BASE_DIR = Path(__file__).resolve().parent if "__file__" in locals() else Path(os.getcwd()).resolve().parent
    DATA_RAW = BASE_DIR / "data" / "raw"
    DATA_PROCESSED = BASE_DIR / "data" / "processed"

    # Enforce directory footprints
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------------------
    # 2. Raw Ingestion & Schema Correction
    # -------------------------------------------------------------------------

    try:
        customers = pd.read_csv(DATA_RAW / "customers.csv")
        cards = pd.read_csv(DATA_RAW / "cards.csv")
        transactions = pd.read_csv(DATA_RAW / "transactions.csv")
    except FileNotFoundError as e:
        print(f"[CRITICAL] Failure during ingestion. Missing resource file: {e}")
        return

    # Enforce proper historical date timeframes
    transactions["transaction_time"] = pd.to_datetime(transactions["transaction_time"])

    print(f"Customers: {customers.shape}, Cards: {cards.shape}, Transactions: {transactions.shape}")

    # -------------------------------------------------------------------------
    # 3. Structural Aggregations & Relational Merges
    # -------------------------------------------------------------------------

    master_df = transactions.merge(customers, on="customer_id", how="left")


    card_metrics = (
        cards.groupby("customer_id")
        .agg(
            number_of_cards=("card_id", "count"),
            max_credit_limit=("credit_limit", "max"),
            avg_credit_limit=("credit_limit", "mean"),
            blocked_cards=("status", lambda x: (x == "Blocked").sum()),
            has_credit_card=("card_type", lambda x: int("Credit" in x.values)),
        )
        .reset_index()
    )

    # Assemble unified staging matrix
    master_df = master_df.merge(card_metrics, on="customer_id", how="left")

    # -------------------------------------------------------------------------
    # 4. Binary Storage Serialization
    # -------------------------------------------------------------------------
    staging_output = DATA_PROCESSED / "stg_master_prepared.parquet"
    print(f"[INFO] Serializing staging matrix data to schema-preserving structure...")
    master_df.to_parquet(staging_output, index=False)
    print(f"[SUCCESS] Stage 1 finalized. Target workspace updated: {staging_output}")

if __name__ == "__main__":
    main()