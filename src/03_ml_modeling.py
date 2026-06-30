#!/usr/bin/env python3
"""
Production Script: Predictive Modeling & Advanced Class Inversion Pipeline
Filename: 03_ml_modeling.py
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    classification_report, 
    roc_auc_score, 
    precision_score, 
    recall_score, 
    f1_score, 
    accuracy_score
)
from xgboost import XGBClassifier

def main():
    # -------------------------------------------------------------------------
    # 1. Environment Routing & Data Ingestion
    # -------------------------------------------------------------------------
    BASE_DIR = Path(__file__).resolve().parent if "__file__" in locals() else Path(os.getcwd()).resolve().parent
    DATA_PROCESSED = BASE_DIR / "data" / "processed"
    IMAGE_DIR = BASE_DIR / "images"

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(DATA_PROCESSED / "stg_features_calculated.parquet")

    # -------------------------------------------------------------------------
    # 2. Structural Cleanup & Feature Value Isolations
    # -------------------------------------------------------------------------
    df["amount_deviation"] = df["amount"] - df["avg_txn_amount"]
    df["amount_to_avg_ratio"] = df["amount"] / (df["avg_txn_amount"] + 1)
    df["transaction_zscore"] = (df["amount"] - df["avg_txn_amount"]) / (df["std_txn_amount"] + 1)
    df["spend_credit_ratio"] = df["amount"] / (df["max_credit_limit"] + 1)
    df["high_amount_anomaly"] = (df["transaction_zscore"] > 3).astype(int)

    DROP_COLS = [
        "is_fraud", "transaction_id", "customer_id", "transaction_time", 
        "join_date", "prev_transaction_time", "fraud_score", "avg_txn_amount", 
        "std_txn_amount", "total_spend", "txn_count", "fraud_count", 
        "fraud_rate", "risk_score", "risk_segment"
    ]

    X = df.drop(columns=DROP_COLS)
    y = df["is_fraud"]

    X["is_active"] = X["is_active"].astype(int)

    categorical_cols = X.select_dtypes(include="object").columns.tolist()
    numerical_cols = X.select_dtypes(exclude="object").columns.tolist()

    # -------------------------------------------------------------------------
    # 3. Train-Test Stratified Validation Splitting
    # -------------------------------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # -------------------------------------------------------------------------
    # 4. Training Dynamic Group Target Risk Mappings
    # -------------------------------------------------------------------------
    train_stg = X_train.copy()
    train_stg["is_fraud"] = y_train

    for col in ["merchant", "channel", "device_type"]:
        risk_map = train_stg.groupby(col)["is_fraud"].mean()
        X_train[f"{col}_risk_score"] = X_train[col].map(risk_map).fillna(0)
        X_test[f"{col}_risk_score"] = X_test[col].map(risk_map).fillna(0)

    for col in ["merchant_risk_score", "channel_risk_score", "device_type_risk_score"]:
        if col not in numerical_cols:
            numerical_cols.append(col)

    # -------------------------------------------------------------------------
    # 5. Pipeline Definition Tier
    # -------------------------------------------------------------------------
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
        ]
    )

    zero_count = len(y_train[y_train == 0])
    one_count = len(y_train[y_train == 1])
    imbalance_ratio = zero_count / one_count

    # -------------------------------------------------------------------------
    # 6. Production Model Fitting & Explicit Operational Classification Threshold
    # -------------------------------------------------------------------------
    xgb_pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", XGBClassifier(
                n_estimators=300,
                max_depth=6,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                scale_pos_weight=imbalance_ratio,
                eval_metric="logloss",
                random_state=42,
                n_jobs=-1
            ))
        ]
    )

    xgb_pipeline.fit(X_train, y_train)

    xgb_probs = xgb_pipeline.predict_proba(X_test)[:, 1]
    
    # Core Global Risk Boundary Rule Constraint Enforced
    FINAL_THRESHOLD = 0.50
    xgb_preds = (xgb_probs >= FINAL_THRESHOLD).astype(int)

    # -------------------------------------------------------------------------
    # 7. System Model Evaluation Matrix
    # -------------------------------------------------------------------------
    print("\n" + "="*50)
    print("TEST PERFORMANCE METRICS EVALUATION")
    print("="*50)
    print(classification_report(y_test, xgb_preds))
    print(f"ROC-AUC Performance Score: {roc_auc_score(y_test, xgb_probs):.4f}\n")

    # -------------------------------------------------------------------------
    # 8. Operationalizing Risk Strategy Threshold Optimization Loops
    # -------------------------------------------------------------------------
    print("="*50)
    print("DECISION THRESHOLD OPTIMIZATION INDEX")
    print("="*50)
    decision_thresholds = [0.30, 0.35, 0.40, 0.45, 0.50]
    threshold_metrics = []

    for t in decision_thresholds:
        y_threshold_preds = (xgb_probs >= t).astype(int)
        threshold_metrics.append({
            "Threshold": t,
            "Precision": precision_score(y_test, y_threshold_preds, zero_division=0),
            "Recall": recall_score(y_test, y_threshold_preds, zero_division=0),
            "F1_Score": f1_score(y_test, y_threshold_preds, zero_division=0),
            "Accuracy": accuracy_score(y_test, y_threshold_preds),
            "Predicted Fraud": y_threshold_preds.sum()
        })

    metrics_df = pd.DataFrame(threshold_metrics)
    print(metrics_df.round(3).to_string(index=False))
    print("\n" + "="*50)

    metrics_output_path = DATA_PROCESSED / "model_threshold_metrics.csv"
    metrics_df.to_csv(metrics_output_path, index=False)

    # -------------------------------------------------------------------------
    # 9. Authentic Transaction Identifier Export Pipeline
    # -------------------------------------------------------------------------
    transaction_ids = df.loc[X_test.index, "transaction_id"]

    ml_predictions = pd.DataFrame({
        "transaction_id": transaction_ids.values,
        "actual_fraud": y_test.values,
        "fraud_probability": xgb_probs,
        "predicted_fraud": xgb_preds
    })

    ml_predictions["risk_segment"] = pd.cut(
        ml_predictions["fraud_probability"],
        bins=[0, 0.25, 0.50, 0.75, 1.0],
        labels=["Low Risk", "Medium Risk", "High Risk", "Critical Risk"]
    )

    output_path = DATA_PROCESSED / "ml_predictions.csv"
    ml_predictions.to_csv(output_path, index=False)

    # -------------------------------------------------------------------------
    # 10. Feature Importance Computations & Standard Document Exports
    # -------------------------------------------------------------------------
    fitted_model = xgb_pipeline.named_steps["model"]
    fitted_preprocessor = xgb_pipeline.named_steps["preprocessor"]

    feature_names = fitted_preprocessor.get_feature_names_out()
    importance_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": fitted_model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    importance_output_path = DATA_PROCESSED / "feature_importance.csv"
    importance_df.to_csv(importance_output_path, index=False)

    plt.figure(figsize=(10, 6))
    plt.barh(importance_df["Feature"].head(15)[::-1], importance_df["Importance"].head(15)[::-1], color="#2b5c8f")
    plt.xlabel("XGBoost Information Gain Metric")
    plt.title("System Predictive Feature Importance Matrix")
    plt.tight_layout()
    
    chart_path = IMAGE_DIR / "feature_importance.png"
    plt.savefig(chart_path, dpi=300)
    plt.close()

if __name__ == "__main__":
    main()