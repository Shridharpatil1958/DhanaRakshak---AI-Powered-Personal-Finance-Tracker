import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def prepare_expense_features(df):
    """Prepare features for expense prediction"""
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    
    # Extract time features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_of_week'] = df['date'].dt.dayofweek
    df['week_of_year'] = df['date'].dt.isocalendar().week
    
    # Create monthly aggregates
    df['year_month'] = df['date'].dt.to_period('M')
    
    return df

def create_time_series_features(df, user_id):
    """Create time series features for a specific user"""
    user_data = df[df['user_id'] == user_id].copy()
    user_data = user_data.sort_values('date')
    
    # Monthly aggregates
    monthly = user_data.groupby(user_data['date'].dt.to_period('M')).agg({
        'amount': 'sum',
        'transaction_type': 'count'
    }).reset_index()
    
    monthly.columns = ['month', 'total_amount', 'transaction_count']
    monthly['month'] = monthly['month'].dt.to_timestamp()
    
    return monthly

def calculate_category_statistics(df, user_id):
    """Calculate category-wise statistics"""
    user_data = df[df['user_id'] == user_id]
    expenses = user_data[user_data['transaction_type'] == 'expense']
    
    category_stats = expenses.groupby('category').agg({
        'amount': ['sum', 'mean', 'std', 'count']
    }).reset_index()
    
    category_stats.columns = ['category', 'total', 'mean', 'std', 'count']
    
    return category_stats

def detect_spending_anomalies(df, user_id):
    """Detect anomalous spending patterns"""
    user_data = df[df['user_id'] == user_id]
    expenses = user_data[user_data['transaction_type'] == 'expense']
    
    anomalies = []
    
    for category in expenses['category'].unique():
        cat_data = expenses[expenses['category'] == category]['amount']
        
        if len(cat_data) < 5:
            continue
        
        mean = cat_data.mean()
        std = cat_data.std()
        
        # Z-score method
        z_scores = np.abs((cat_data - mean) / std)
        anomaly_indices = z_scores[z_scores > 3].index
        
        for idx in anomaly_indices:
            anomalies.append({
                'date': expenses.loc[idx, 'date'],
                'category': category,
                'amount': expenses.loc[idx, 'amount'],
                'z_score': z_scores[idx]
            })
    
    return anomalies

def calculate_savings_rate(df, user_id):
    """Calculate savings rate for a user"""
    user_data = df[df['user_id'] == user_id]
    
    total_income = user_data[user_data['transaction_type'] == 'income']['amount'].sum()
    total_expense = user_data[user_data['transaction_type'] == 'expense']['amount'].sum()
    
    if total_income > 0:
        savings_rate = ((total_income - total_expense) / total_income) * 100
        return max(0, savings_rate)
    
    return 0

def predict_next_month_expense(monthly_data, periods=1):
    """Simple moving average prediction for next month expense"""
    if len(monthly_data) < 3:
        return monthly_data['total_amount'].mean() if len(monthly_data) > 0 else 0
    
    # Use last 3 months average
    recent_avg = monthly_data['total_amount'].tail(3).mean()
    
    # Add trend component
    if len(monthly_data) >= 6:
        recent_trend = monthly_data['total_amount'].tail(3).mean()
        older_trend = monthly_data['total_amount'].tail(6).head(3).mean()
        trend = recent_trend - older_trend
        prediction = recent_avg + (trend * 0.5)
    else:
        prediction = recent_avg
    
    return max(0, prediction)