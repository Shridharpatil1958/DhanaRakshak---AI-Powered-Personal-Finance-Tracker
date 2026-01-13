import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def train_expense_predictor(df):
    """Train expense prediction model"""
    print("Training Expense Predictor...")
    
    # Prepare data
    expenses = df[df['transaction_type'] == 'expense'].copy()
    expenses['date'] = pd.to_datetime(expenses['date'])
    
    # Create features
    expenses['month'] = expenses['date'].dt.month
    expenses['day_of_week'] = expenses['date'].dt.dayofweek
    expenses['day'] = expenses['date'].dt.day
    
    # Encode category
    le_category = LabelEncoder()
    expenses['category_encoded'] = le_category.fit_transform(expenses['category'])
    
    # Features and target
    features = ['month', 'day_of_week', 'day', 'category_encoded', 'user_id']
    X = expenses[features]
    y = expenses['amount']
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X, y)
    
    # Save model and encoder
    joblib.dump(model, 'models/expense_predictor.pkl')
    joblib.dump(le_category, 'models/category_encoder.pkl')
    
    print(f"✓ Expense Predictor trained (Score: {model.score(X, y):.3f})")
    return model

def train_savings_predictor(df):
    """Train savings prediction model"""
    print("Training Savings Predictor...")
    
    # Calculate monthly savings per user
    df['date'] = pd.to_datetime(df['date'])
    df['year_month'] = df['date'].dt.to_period('M')
    
    monthly_data = []
    for user_id in df['user_id'].unique():
        user_df = df[df['user_id'] == user_id]
        
        for period in user_df['year_month'].unique():
            period_data = user_df[user_df['year_month'] == period]
            
            income = period_data[period_data['transaction_type'] == 'income']['amount'].sum()
            expense = period_data[period_data['transaction_type'] == 'expense']['amount'].sum()
            savings = income - expense
            
            monthly_data.append({
                'user_id': user_id,
                'month': period.month,
                'income': income,
                'expense': expense,
                'savings': savings
            })
    
    savings_df = pd.DataFrame(monthly_data)
    
    # Features and target
    X = savings_df[['user_id', 'month', 'income', 'expense']]
    y = savings_df['savings']
    
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Save model
    joblib.dump(model, 'models/savings_predictor.pkl')
    
    print(f"✓ Savings Predictor trained (Score: {model.score(X, y):.3f})")
    return model

def train_bills_estimator(df):
    """Train upcoming bills estimation model"""
    print("Training Bills Estimator...")
    
    # Filter bill transactions
    bill_categories = ['Bills', 'Rent']
    bills = df[df['category'].isin(bill_categories)].copy()
    bills['date'] = pd.to_datetime(bills['date'])
    
    # Create features
    bills['month'] = bills['date'].dt.month
    bills['day'] = bills['date'].dt.day
    
    # Encode category
    le_category = LabelEncoder()
    bills['category_encoded'] = le_category.fit_transform(bills['category'])
    
    # Features and target
    features = ['user_id', 'month', 'day', 'category_encoded']
    X = bills[features]
    y = bills['amount']
    
    # Train model
    model = RandomForestRegressor(n_estimators=50, random_state=42, max_depth=8)
    model.fit(X, y)
    
    # Save model and encoder
    joblib.dump(model, 'models/bills_estimator.pkl')
    joblib.dump(le_category, 'models/bills_category_encoder.pkl')
    
    print(f"✓ Bills Estimator trained (Score: {model.score(X, y):.3f})")
    return model

def train_anomaly_detector(df):
    """Train anomaly detection model"""
    print("Training Anomaly Detector...")
    
    # Prepare expense data
    expenses = df[df['transaction_type'] == 'expense'].copy()
    
    # Create features
    features_data = []
    for user_id in expenses['user_id'].unique():
        user_expenses = expenses[expenses['user_id'] == user_id]
        
        for category in user_expenses['category'].unique():
            cat_expenses = user_expenses[user_expenses['category'] == category]['amount']
            
            if len(cat_expenses) >= 5:
                features_data.append({
                    'user_id': user_id,
                    'mean_amount': cat_expenses.mean(),
                    'std_amount': cat_expenses.std(),
                    'max_amount': cat_expenses.max(),
                    'min_amount': cat_expenses.min()
                })
    
    features_df = pd.DataFrame(features_data)
    X = features_df[['mean_amount', 'std_amount', 'max_amount', 'min_amount']]
    
    # Train Isolation Forest
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(X)
    
    # Save model
    joblib.dump(model, 'models/anomaly_detector.pkl')
    
    print("✓ Anomaly Detector trained")
    return model

def train_budget_recommender(df):
    """Train budget recommendation model"""
    print("Training Budget Recommender...")
    
    # Calculate category-wise spending patterns
    expenses = df[df['transaction_type'] == 'expense'].copy()
    
    budget_data = []
    for user_id in expenses['user_id'].unique():
        user_expenses = expenses[expenses['user_id'] == user_id]
        total_expense = user_expenses['amount'].sum()
        
        for category in user_expenses['category'].unique():
            cat_expense = user_expenses[user_expenses['category'] == category]['amount'].sum()
            percentage = (cat_expense / total_expense) * 100
            
            budget_data.append({
                'user_id': user_id,
                'category': category,
                'total_expense': total_expense,
                'category_expense': cat_expense,
                'percentage': percentage
            })
    
    budget_df = pd.DataFrame(budget_data)
    
    # Encode category
    le_category = LabelEncoder()
    budget_df['category_encoded'] = le_category.fit_transform(budget_df['category'])
    
    # Features and target
    X = budget_df[['user_id', 'category_encoded', 'total_expense']]
    y = budget_df['category_expense']
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X, y)
    
    # Save model and encoder
    joblib.dump(model, 'models/budget_recommender.pkl')
    joblib.dump(le_category, 'models/budget_category_encoder.pkl')
    
    print(f"✓ Budget Recommender trained (Score: {model.score(X, y):.3f})")
    return model

def main():
    """Main training function"""
    print("="*50)
    print("DhanaRakshak ML Model Training")
    print("="*50)
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    # Check for existing dataset
    if os.path.exists('dhanarakshak_large_dataset.csv'):
        print("\nLoading existing dataset...")
        df = pd.read_csv('dhanarakshak_large_dataset.csv')

    print(f"Dataset loaded: {len(df)} records")
    print(f"Users: {df['user_id'].nunique()}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    
    # Train all models
    print("\n" + "="*50)
    print("Training Models...")
    print("="*50 + "\n")
    
    train_expense_predictor(df)
    train_savings_predictor(df)
    train_bills_estimator(df)
    train_anomaly_detector(df)
    train_budget_recommender(df)
    
    print("\n" + "="*50)
    print("✓ All models trained successfully!")
    print("="*50)

if __name__ == '__main__':
    main()