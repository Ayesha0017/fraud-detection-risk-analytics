import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
from collections import defaultdict

fake = Faker()

np.random.seed(42)
random.seed(42)

NUM_CUSTOMERS = 2000
NUM_TRANSACTIONS = 50000
TARGET_FRAUD_RATE = 0.012 

CITIES = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Pune", "Kolkata", "Ahmedabad"]

CITY_COORDINATES = {
    "Mumbai": (19.0760, 72.8777), "Delhi": (28.6139, 77.2090),
    "Bangalore": (12.9716, 77.5946), "Hyderabad": (17.3850, 78.4867),
    "Chennai": (13.0827, 80.2707), "Pune": (18.5204, 73.8567),
    "Kolkata": (22.5726, 88.3639), "Ahmedabad": (23.0225, 72.5714)
}

MERCHANT_CATEGORIES = {
    "Groceries": (100, 5000, 0.5), "Electronics": (2000, 150000, 1.5),
    "Food Delivery": (100, 2000, 0.3), "Travel": (3000, 100000, 1.2),
    "Fuel": (300, 6000, 0.4), "Shopping Mall": (500, 50000, 1.0),
    "Restaurant": (500, 15000, 0.6), "Entertainment": (300, 8000, 0.7),
    "Healthcare": (500, 30000, 0.4), "Education": (1000, 50000, 0.3),
    "Gaming": (500, 20000, 2.0), "Cryptocurrency": (5000, 200000, 2.5)
}

MERCHANT_RISK = {
    "Groceries": 0.3, "Electronics": 0.8, "Food Delivery": 0.2,
    "Travel": 0.7, "Fuel": 0.3, "Shopping Mall": 0.5,
    "Restaurant": 0.4, "Entertainment": 0.5, "Healthcare": 0.2,
    "Education": 0.2, "Gaming": 1.2, "Cryptocurrency": 2.0
}

print("Generating customers...")
customers_data = []

for customer_id in range(1, NUM_CUSTOMERS + 1):
    age = np.random.randint(18, 80)
    
    if np.random.rand() < 0.7:
        income = np.random.lognormal(10.8, 0.6)
    else:
        income = np.random.lognormal(12.0, 0.8)
    
    income = round(max(income * 1000, 15000), 2)
    
    if income < 30000:
        account_type = "Savings"
    elif income < 100000:
        account_type = np.random.choice(["Savings", "Current"], p=[0.7, 0.3])
    else:
        account_type = np.random.choice(["Current", "Premium"], p=[0.6, 0.4])
    
    join_date = fake.date_between(start_date='-10y', end_date='today')
    tenure_days = (datetime.now().date() - join_date).days
    
    risk_factors = sum([
        tenure_days < 90,
        account_type == "Premium",
        age < 25 or age > 70
    ])
    risk_score = min(risk_factors * 0.15 + np.random.uniform(0, 0.1), 0.5)
    
    customers_data.append({
        "customer_id": customer_id, "age": age, "income": income,
        "city": np.random.choice(CITIES), "account_type": account_type,
        "join_date": join_date, "tenure_days": tenure_days,
        "risk_score": round(risk_score, 3), "is_active": np.random.rand() < 0.95
    })

customers = pd.DataFrame(customers_data)

print("Generating cards...")
cards_data = []

for _, customer in customers.iterrows():
    num_cards = 1 if customer['income'] < 50000 else np.random.choice([1, 2], p=[0.6, 0.4])
    
    for _ in range(num_cards):
        card_type = np.random.choice(["Debit", "Credit"], p=[0.75, 0.25])
        credit_limit = customer['income'] * (np.random.uniform(1.5, 4) if card_type == "Credit" else 0.8)
        status = np.random.choice(["Active", "Blocked", "Compromised"], p=[0.92, 0.05, 0.03])
        
        cards_data.append({
            "card_id": fake.uuid4(),
            "customer_id": customer['customer_id'],
            "card_type": card_type,
            "credit_limit": round(credit_limit, 2),
            "status": status
        })

cards = pd.DataFrame(cards_data)

print("Generating transactions...")
customer_patterns = {}
for _, customer in customers.iterrows():
    customer_patterns[customer['customer_id']] = {
        'weekday_ratio': np.random.uniform(0.65, 0.85),
        'favorite_merchants': random.sample(list(MERCHANT_CATEGORIES.keys()), k=np.random.randint(3, 7)),
        'income_factor': min(customer['income'] / 50000, 3.0),
        'base_risk': customer['risk_score']
    }

merchant_list = list(MERCHANT_CATEGORIES.keys())
merchant_ranges = {m: MERCHANT_CATEGORIES[m] for m in merchant_list}

transactions_data = []
customer_history = defaultdict(lambda: {
    'avg_amount_30d': 1000, 'usual_merchants': [], 'last_txn_time': None,
    'last_location': None, 'txn_count_today': 0, 'last_txn_day': None
})

start_date = datetime(2024, 1, 1)
total_days = 365
fraud_count = 0
expected_frauds = int(NUM_TRANSACTIONS * TARGET_FRAUD_RATE)

hours = list(range(24))
hour_probs = [0.02] * 24
for h in range(8, 21):
    hour_probs[h] = 0.06
hour_probs = [p/sum(hour_probs) for p in hour_probs]

for txn_id in range(1, NUM_TRANSACTIONS + 1):
    if txn_id % 10000 == 0:
        print(f"   Progress: {txn_id}/{NUM_TRANSACTIONS} logs completed. (Fraud pool: {fraud_count})")
    
    customer = customers.sample(1).iloc[0]
    customer_id = customer['customer_id']
    pattern = customer_patterns[customer_id]
    
    day_offset = np.random.randint(0, total_days)
    hour = int(np.random.choice(hours, p=hour_probs))
    txn_time = start_date + timedelta(days=int(day_offset), hours=hour, minutes=int(np.random.randint(0, 60)))
    day_of_week = txn_time.weekday()
    
    if day_of_week < 5:
        if np.random.rand() > pattern['weekday_ratio'] and np.random.rand() < 0.3:
            continue
    else:
        if np.random.rand() < pattern['weekday_ratio'] and np.random.rand() < 0.3:
            continue
    
    if np.random.rand() < 0.7 and pattern['favorite_merchants']:
        merchant = np.random.choice(pattern['favorite_merchants'])
    else:
        merchant = np.random.choice(merchant_list)
    
    low, high, _ = merchant_ranges[merchant]
    amount = np.random.uniform(low, high) * (pattern['income_factor'] ** 0.3)
    amount = float(round(max(50, min(amount, customer['income'] * 0.3)), 2))
    
    if merchant == "Cryptocurrency":
        channel = "NetBanking"
    elif merchant in ["Food Delivery", "Groceries"]:
        channel = np.random.choice(["UPI", "Card"], p=[0.7, 0.3])
    else:
        channel = np.random.choice(["UPI", "Card", "NetBanking"], p=[0.45, 0.4, 0.15])
    
    if customer['age'] > 60:
        device = np.random.choice(["Web", "Android"], p=[0.6, 0.4])
    elif customer['income'] > 100000:
        device = np.random.choice(["iPhone", "Android", "Web"], p=[0.5, 0.4, 0.1])
    else:
        device = np.random.choice(["Android", "Web", "iPhone"], p=[0.6, 0.3, 0.1])
    
    location = customer['city']
    distance = 0
    if np.random.rand() < 0.05:
        other_cities = [c for c in CITIES if c != customer['city']]
        if other_cities:
            location = np.random.choice(other_cities)
            distance = 100
    
    # ---------------------------------------------------
    # REFACTORED FRAUD DETECTION LABELLING
    # ---------------------------------------------------
    fraud_score = 0
    history = customer_history[customer_id]
    
    if amount > history['avg_amount_30d'] * 8:
        fraud_score += 6
    elif amount > history['avg_amount_30d'] * 5:
        fraud_score += 4
    elif amount > history['avg_amount_30d'] * 3:
        fraud_score += 2

    if hour <= 4:
        fraud_score += 4
    elif hour <= 6:
        fraud_score += 2

    if merchant == "Cryptocurrency":
        fraud_score += 6
    elif merchant == "Gaming":
        fraud_score += 3
    elif merchant == "Travel":
        fraud_score += 2

    if distance > 0:
        fraud_score += 3

    if history['last_location'] and history['last_txn_time']:
        time_diff_hours = (txn_time - history['last_txn_time']).total_seconds() / 3600
        if location != history['last_location']:
            if time_diff_hours < 1:
                fraud_score += 10
            elif time_diff_hours < 3:
                fraud_score += 7
            elif time_diff_hours < 6:
                fraud_score += 4

    if history['last_txn_day'] == txn_time.day:
        history['txn_count_today'] += 1
        if history['txn_count_today'] > 15:
            fraud_score += 6
        elif history['txn_count_today'] > 10:
            fraud_score += 4
        elif history['txn_count_today'] > 5:
            fraud_score += 2
    else:
        history['txn_count_today'] = 1
        history['last_txn_day'] = txn_time.day

    customer_cards = cards[cards['customer_id'] == customer_id]
    if len(customer_cards) > 0:
        card_status = customer_cards['status'].iloc[0]
        if card_status == "Compromised":
            fraud_score += 8
        elif card_status == "Blocked":
            fraud_score += 4

    if pattern['base_risk'] > 0.3:
        fraud_score += 2

    # Map target risk score ranges explicitly to split distributions cleanly
    if fraud_score >= 20:
        fraud_probability = 0.95
    elif fraud_score >= 15:
        fraud_probability = 0.75
    elif fraud_score >= 10:
        fraud_probability = 0.40
    elif fraud_score >= 7:
        fraud_probability = 0.15
    elif fraud_score >= 4:
        fraud_probability = 0.05
    else:
        fraud_probability = 0.003

    is_fraud = 1 if np.random.rand() < fraud_probability else 0
    
    if is_fraud:
        fraud_count += 1
    
    transactions_data.append({
        "transaction_id": txn_id, "customer_id": int(customer_id), "amount": amount,
        "merchant": merchant, "channel": channel, "device_type": device,
        "transaction_time": txn_time, "location": location, "is_fraud": is_fraud,
        "fraud_score": fraud_score, "hour": hour, "day_of_week": int(day_of_week),
        "distance_from_home": distance
    })
    
    history['avg_amount_30d'] = history['avg_amount_30d'] * 0.95 + amount * 0.05
    history['last_txn_time'] = txn_time
    history['last_location'] = location
    
    if merchant not in history['usual_merchants'] and len(history['usual_merchants']) < 8:
        history['usual_merchants'].append(merchant)

transactions = pd.DataFrame(transactions_data)

print("Calculating aggregates...")
customer_aggregates = transactions.groupby('customer_id').agg({
    'amount': ['mean', 'std', 'sum', 'count'],
    'is_fraud': 'sum'
}).round(2)

customer_aggregates.columns = ['avg_txn_amount', 'std_txn_amount', 'total_spend', 'txn_count', 'fraud_count']

customers = customers.merge(customer_aggregates, on='customer_id', how='left')
customers = customers.fillna({'avg_txn_amount': 1000, 'txn_count': 0, 'fraud_count': 0})
customers['fraud_rate'] = customers['fraud_count'] / customers['txn_count']

print("\nSaving files...")
customers.to_csv(r"data\raw\customers.csv", index=False)
cards.to_csv(r"data\raw\cards.csv", index=False)
transactions.to_csv(r"data\raw\transactions.csv", index=False)

print("\n" + "="*50)
print("✅ GENERATION COMPLETE!")
print("="*50)
print(f"Customers: {len(customers):,}")
print(f"Cards: {len(cards):,}")
print(f"Transactions: {len(transactions):,}")
print(f"Total Fraudulent Logs: {transactions['is_fraud'].sum():,}")
print(f"Calculated Fraud Rate: {transactions['is_fraud'].mean()*100:.2f}%")