# Banking Fraud Detection & Transaction Risk Analytics Platform

An end-to-end financial analytics and machine learning solution designed to identify suspicious transactions, monitor customer risk profiles, and empower fraud prevention teams with actionable, data-driven insights.

---

## Project Structure

FRAUD_DETECTION/
│
├── README.md
│
├── sql/
│   ├── 01_database_setup.sql
│   ├── 02_data_quality_checks.sql
│   ├── 03_fraud_kpis.sql
│   ├── 04_customer_risk_analysis.sql
│   ├── 05_merchant_channel_analysis.sql
│   ├── 06_behavioral_fraud_analysis.sql
│   ├── 07_anomaly_detection_queries.sql
│   ├── 08_time_series_analysis.sql
│   └── 09_powerbi_views.sql
│
├── src/
│   ├── 01_data_preparation.py
│   ├── 02_risk_scoring_engine.py
│   ├── 03_ml_modeling.py
│   └── dataset.py
│
├── notebooks/
│   ├── 01_data_preparation.ipynb
│   └── 02_risk_scoring_engine.ipynb
│
├── output_tables/
│   ├── vw_channel_risk.csv
│   ├── vw_customer_risk_summary.csv
│   ├── vw_daily_fraud_trend.csv
│   ├── vw_device_risk.csv
│   ├── vw_fraud_loss_contribution.csv
│   ├── vw_fraud_overview.csv
│   ├── vw_hourly_fraud.csv
│   ├── vw_location_risk.csv
│   ├── vw_merchant_risk.csv
│   ├── vw_risk_segment_summary.csv
│   └── vw_transaction_velocity.csv
│
├── data/
│   └── processed/
│       ├── customer_risk_segments.csv
│       ├── ml_predictions.csv
│       └── xgboost_feature_importances.csv
│
└── images/
    ├── Fraud_overview_and_financial_impact.png
    ├── Behavioral_analytics.png
    ├── Risk_monitoring_and_segmentation.png
    └── ml_monitoring.png

## 📌 Table of Contents
- [Project Overview](#project-overview)
- [Workflow Architecture](#workflow-architecture)
- [Dataset Specifications](#dataset-specifications)
- [SQL Analytics Layer](#sql-analytics-layer)
- [Risk Scoring Framework](#risk-scoring-framework)
- [Machine Learning & Predictive Modeling](#machine-learning--predictive-modeling)
- [Power BI Executive Dashboard](#power-bi-executive-dashboard)
- [Strategic Business Recommendations](#strategic-business-recommendations)
- [Technology Stack](#technology-stack)
- [Project Outcomes](#project-outcomes)

---

## 🛠 Project Overview
Financial fraud represents a major operational and financial vulnerability for modern digital banking institutions. Traditional rule-based systems often struggle to scale against rapidly changing, complex fraud strategies, resulting in high false-positive rates, revenue loss, and friction in the customer experience.

This platform replaces rigid logic with a hybrid analytics solution combining **deep SQL profiling**, a **dynamic Behavioral Risk Scoring engine**, and **advanced Machine Learning (XGBoost)** to flag suspicious activity, segment customers by operational risk, and structure proactive transaction surveillance.

---

## 🏗 Workflow Architecture

```
  +------------------+      +-------------------+      +-------------------------+
  | Business Problem | ---> |   SQL Analytics   | ---> | Risk Scoring Framework  |
  +------------------+      +-------------------+      +-------------------------+
                                                                    |
                                                                    v
  +------------------+      +-------------------+      +-------------------------+
  |  Business Recs   | <--- | Exec Dashboards   | <--- |   Behavioral & ML Engine|
  +------------------+      +-------------------+      +-------------------------+
```

### Data Pipelines & Integration Map
```
Customers  🎨
Cards      💳 ----> [ SQL Analytics Views ] ----> [ Risk Engine ] ----> [ ML Models ] ----> [ Power BI ]
Trans.     🛍️
```

---

## 📊 Dataset Specifications
The platform ingests and correlates data from three core relational business tables:

### 🏠 1. Customers
* `customer_id` (Primary Key)
* `age` / `income` / `city`
* `account_type` (e.g., Savings, Current)
* `join_date`

### 💳 2. Cards
* `card_id` (Primary Key)
* `customer_id` (Foreign Key)
* `card_type` (e.g., Platinum, Gold)
* `credit_limit`
* `status` (Active, Blocked)

### 🛍️ 3. Transactions
* `transaction_id` (Primary Key)
* `customer_id` (Foreign Key)
* `amount` / `merchant` / `channel` (NetBanking, Card, UPI)
* `device_type` (iPhone, Android, Web)
* `transaction_time` / `location`
* `distance_from_home` (Calculated distance parameter in km)
* `is_fraud` (Target Label: 1 = Fraud, 0 = Normal)

### 📈 Global System Statistics
| Metric | Structural Value |
| :--- | :--- |
| **Total Unique Customers** | 2,000 |
| **Total Cards Issued** | 2,801 |
| **Total Historical Transactions Evaluated** | 44,217 |
| **Identified Fraud Events** | 4,515 |
| **Baseline System Fraud Rate** | **10.21%** |

---

## 🔍 SQL Analytics Layer
A optimized analytics tier was implemented within the database engine to isolate behavior baselines, optimize execution queries, and export aggregate data abstractions for ingestion into BI dashboards.

### 💰 Core Fraud Financials
* **Total Checked Volume:** 44,217 transactions
* **Total Fraudulent Volume:** 4,515 transactions
* **Aggregate Financial Fraud Exposure Loss:** **$380.07M**
* **Average Ticket Size (Fraudulent):** **$84.18K**

---

### 🏬 Sector Risk Breakdown
```
Cryptocurrency  ========================================= [40.10%]  🔥 Critical Risk
Travel          =============== [15.34%]
Electronics     =========== [11.14%]
Gaming          ========== [10.51%]
Shopping Mall   ======== [7.96%]
Education       ======== [7.87%]
Healthcare      ====== [6.35%]
```
> 💡 **Key Insight:** Cryptocurrency transactions exhibit severe exposure, with breach velocities nearly **4x higher** than the baseline bank average.

---

### 📡 Channel & Device Vulnerabilities

#### Payment Channel Risk Profile
| Channel | Transaction Share Fraud Rate | Risk Exposure Classification |
| :--- | :---: | :--- |
| **NetBanking** | **22.50%** | 🔴 Severe High Exposure |
| **Card** | 7.41% | 🟡 Baseline Operational |
| **UPI** | 7.01% | 🟢 Low Relative Risk |

#### User Access Endpoint Risk Profile
| Device Type | System Fraud Rate | Variance vs. Baseline |
| :--- | :---: | :---: |
| **iPhone** | 10.25% | +0.04% |
| **Android** | 10.22% | +0.01% |
| **Web Browser** | 10.15% | -0.06% |

> 💡 **Key Insight:** Payment endpoints (NetBanking) are highly predictive vectors—showing a **3x risk expansion** over Cards/UPI. Conversely, physical device choice shows minimal variance and acts as a neutral variable.

---

### ⏰ Chronological & Geographic Anomaly Patterns

#### Critical Chronological Windows (Top 5 Hours)
1.  **01:00 AM** — `23.44%` Fraud Probability
2.  **00:00 AM** — `22.57%` Fraud Probability
3.  **02:00 AM** — `21.36%` Fraud Probability
4.  **04:00 AM** — `19.91%` Fraud Probability
5.  **03:00 AM** — `19.56%` Fraud Probability

#### Behavioral Anomalies (Normal vs. Fraud)
* **Geographic Displacement (Avg Distance from Home):**
    * *Normal Transactions:* **3.4 km**
    * *Fraudulent Transactions:* **18.7 km** 🚨 *(~6x increase)*
* **Financial Velocity Vector (Avg Transaction Ticket Size):**
    * *Normal Transactions:* **$32.57K**
    * *Fraudulent Transactions:* **$84.18K** 🚨 *(~2.6x increase)*

---

## 🧮 Risk Scoring Framework
To convert raw descriptive analytical flags into real-time operational decisions, the platform computes a complex weighted **Risk Score** for every transaction across five dimensions:

$$	ext{Risk Score} = f(	ext{Amount Risk}, 	ext{Merchant Risk}, 	ext{Distance Risk}, 	ext{Time Risk}, 	ext{Device Risk})$$

Based on their cumulative transactional scoring indices, user profiles are stratified into operational action bands:

### Risk Segment Separation Matrix
| Operational Risk Segment | Customer Account Vol | Segment Fraud Velocity Rate | Strategic Control Status |
| :--- | :---: | :---: | :--- |
| 🟢 **Low Risk** | 13,900 | 2.51% | Whitelisted / Auto-Approve |
| 🟡 **Medium Risk** | 21,952 | 7.81% | Passive Monitoring / Standard Thresholds |
| 🟠 **High Risk** | 7,640 | 26.39% | Step-up MFA / Velocity Limits Enforced |
| 🔴 **Critical Risk** | 725 | **60.14%** | Immediate Hard Freeze / Manual Queue Routing |

> 📌 **Framework Validation:** The framework achieves excellent segment separation. It successfully groups highly vulnerable profiles, capturing a **>60% fraud rate** within the designated Critical Risk segment.

---

## 🤖 Machine Learning & Predictive Modeling
The platform implements supervised machine learning to predict transaction-level fraud threats by processing both core raw variables and engineered behavioral features.

### Candidate Algorithms Evaluated
* **Logistic Regression:** Baseline setup utilizing synthetic class weighting parameters to counter the major class imbalance (10.21% minority mix).
* **Random Forest:** Deployed to handle non-linear interactions across spatial displacements and merchant vectors.
* **XGBoost (Selected Production Model):** Deployed due to its superior gradient-boosted decision tree optimization framework and low latency inference.
* **Isolation Forest:** Unsupervised benchmark structure to evaluate pure out-of-distribution behavioral anomalies.

### 📈 Chosen Model Performance Profile: XGBoost
| Validation Criterion | Statistical Value | Operational Impact |
| :--- | :---: | :--- |
| **ROC-AUC** | **0.844** | Strong overall discriminatory power |
| **Recall (Sensitivity)** | **66%** | Captures 2 out of every 3 true fraud patterns natively |
| **Precision** | **34%** | Managed false-positive ratio (approx. 2:1 ratio for ops triage) |
| **Flagged Transactions** | 1,740 | Streamlined queue footprint for internal analysts |
| **True Positive Catch** | 598 | Highly verified financial saves within the test subset |

### 🔝 Feature Importance Hierarchy (Top 10 Indicators)
1.  `Merchant_Category_Cryptocurrency` (Categorical Flag)
2.  `High_Distance_Flag` (Engineered Boolean Indicator)
3.  `Merchant_Risk_Score` (Engineered Historical Aggregation)
4.  `Distance_From_Home` (Continuous Metric)
5.  `Card_Status_Blocked` (Historical Account Status Vector)
6.  `Transaction_Hour` (Cyclical Time Point)
7.  `Amount_Deviation` (Delta vs. Customer Rolling Average)
8.  `Merchant_Category_Gaming` (Categorical Flag)
9.  `Merchant_Category_Food_Delivery` (Categorical Flag)
10. `Night_Transaction_Flag` (Engineered Time-Window Boolean)

---

## 📊 Power BI Executive Dashboard
The system delivers automated, cross-functional visibility through a curated four-page business intelligence suite.

### 📑 Page 1 — Fraud Overview & Financial Impact
* **Core Performance Metrics:** Total System Vol, Fraud Events, System Fraud Rate, Aggregate Financial Loss ($380.07M), Average Ticket Size.
* **Analytical Graphics:** Daily Fraud Trendlines, Chronological Loss Accumulation, Multi-Channel Risk Breakdown, Endpoint Device Cross-Tabulations.
* *Visual Placeholder:* `[]`

### 📑 Page 2 — Behavioral Analytics Deep-Dive
* **Core Performance Metrics:** Fraudulent vs Standard Size Deltas, Spatial Displacement Indicators (Fraudulent vs Standard Distances).
* **Analytical Graphics:** Merchant Category Matrix, Geospatial Heatmaps, Hour-of-Day Activity Grids, Behavioral Insight Alerts Pane.
* *Visual Placeholder:* `[INSERT PAGE 2 DASHBOARD SCREENSHOT HERE]`

### 📑 Page 3 — Risk Monitoring & Segmentation
* **Core Performance Metrics:** Total Active High-Risk Customers, Active Critical-Risk Customers, Average System Risk Score, Critical Cohort Fraud Velocity.
* **Analytical Graphics:** Account Risk Population Curves, Fraud Volatility by Segment, High-Risk Surveillance Queue, Operational Action Indicators.
* *Visual Placeholder:* `[INSERT PAGE 3 DASHBOARD SCREENSHOT HERE]`

### 📑 Page 4 — Machine Learning & Pipeline Audits
* **Core Performance Metrics:** Validation ROC-AUC (0.844), Model Recall, Model Precision, Automated Predictions Generated, True Positive Verification Count.
* **Analytical Graphics:** Confusion Matrix Breakdown, Probability Density Curves, XGBoost Global Feature Weightings, High-Priority Auto-Generated Investigation Queue.
* *Visual Placeholder:* `[INSERT PAGE 4 DASHBOARD SCREENSHOT HERE]`

---

## 🚀 Strategic Business Recommendations

### 🪙 1. Enforce Hard Controls on Cryptocurrency Merchants
* **Finding:** Crypto purchases show extreme risk exposure (40.10% fraud velocity).
* **Action Plan:** Implement mandatory Multi-Factor Authentication (MFA) prompts for all outbound cryptocurrency transfers. Automatically hold transactions exceeding $10k for out-of-band confirmation.

### 🌌 2. Deploy Automated Midnight Velocity Fences
* **Finding:** Over 20% of midnight-to-dawn transactions (00:00–05:00) are fraudulent.
* **Action Plan:** Enforce strict velocity caps ($500 aggregate limits) during these hours. Dynamic risk scoring should trigger automated step-up confirmation calls or biometrics for late-night deviations.

### 📍 3. Dynamic Location Profiles via Geo-Fencing
* **Finding:** Fraud locations average 18.7 km away from a customer's core baseline location, compared to 3.4 km for standard transactions.
* **Action Plan:** Integrate real-time geographic calculation rules within core validation engines. Flag and hold cards when transactions are initialized outside the customer's typical operating radius until authorized via push notifications.

### 🔴 4. Institutionalize Continuous Risk Scanning
* **Finding:** The Critical Risk customer group contains an active fraud rate above 60%.
* **Action Plan:** Run automated batch processing hourly to refresh risk scores. Instantly limit accounts that move into the Critical Risk band, minimizing exposure before a malicious transaction occurs.

### ⚖️ 5. Operationalize Model-Assisted Queue Management
* **Finding:** Pure rule-based configurations create significant operational noise and high false positives.
* **Action Plan:** Route investigations using the XGBoost model's raw fraud probabilities. Sorting the queue by model confidence allows risk teams to focus on high-probability incidents first, maximizing capital recovery per analyst hour.

---

## 💻 Technology Stack
* **Structured Storage & Aggregation:** Microsoft SQL Server (Transact-SQL optimization layers, relational views, and indexes).
* **Data Science Pipeline:** Python 3.x (Pandas, NumPy for data manipulation).
* **Machine Learning Suite:** Scikit-Learn, XGBoost Architecture, Hyperparameter Optimization tools.
* **Visualizations & Reporting:** Matplotlib, Seaborn (exploratory plotting), Power BI Desktop (enterprise interactive dashboard delivery).

---

## 🎯 Project Outcomes
The platform provides a complete Banking Fraud Detection & Transaction Risk Analytics system. By combining deep SQL profiling, custom behavioral risk scoring, and machine learning, it effectively identifies fraud patterns, segments customer risk profiles, and helps fraud teams scale their operations. 

The production **XGBoost model achieved a strong ROC-AUC of 0.844**, while the custom risk engine accurately isolated highly vulnerable profiles—capturing a **fraud rate exceeding 60% within the designated Critical Risk segment**. This provides the institution with clear, reliable protection against ongoing financial exposure.