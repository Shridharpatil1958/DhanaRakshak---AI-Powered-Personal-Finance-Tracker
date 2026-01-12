from flask import Blueprint, request, jsonify, session
import joblib
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from routes.auth import token_required
from utils.db_utils import DatabaseManager
from ml.model_utils import create_time_series_features, predict_next_month_expense

api_bp = Blueprint('api', __name__)

# Load models at startup
MODELS = {}

def load_models():
    """Load all trained models"""
    global MODELS
    
    model_files = {
        'expense_predictor': 'models/expense_predictor.pkl',
        'savings_predictor': 'models/savings_predictor.pkl',
        'bills_estimator': 'models/bills_estimator.pkl',
        'anomaly_detector': 'models/anomaly_detector.pkl',
        'budget_recommender': 'models/budget_recommender.pkl',
        'category_encoder': 'models/category_encoder.pkl',
        'bills_category_encoder': 'models/bills_category_encoder.pkl',
        'budget_category_encoder': 'models/budget_category_encoder.pkl'
    }
    
    for name, path in model_files.items():
        if os.path.exists(path):
            MODELS[name] = joblib.load(path)
            print(f"✓ Loaded {name}")
        else:
            print(f"✗ Model not found: {path}")

@api_bp.route('/api/predict/expenses', methods=['POST'])
@token_required
def predict_expenses():
    """Predict next month's expenses"""
    try:
        user_id = session.get('user_id')
        
        # Get user transactions
        query = """
            SELECT date, transaction_type, amount, category
            FROM transactions
            WHERE user_id = %s AND transaction_type = 'expense'
            ORDER BY date DESC
            LIMIT 500
        """
        transactions = DatabaseManager.execute_query(query, (user_id,), fetch=True)
        
        if not transactions or len(transactions) < 3:
            return jsonify({
                'success': False,
                'message': 'Insufficient data for prediction. Please add more transactions.'
            })
        
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        
        # Create monthly aggregates
        monthly_data = create_time_series_features(df.assign(user_id=user_id), user_id)
        
        # Predict next month
        prediction = predict_next_month_expense(monthly_data)
        
        # Calculate confidence based on data consistency
        if len(monthly_data) >= 3:
            recent_std = monthly_data['total_amount'].tail(3).std()
            recent_mean = monthly_data['total_amount'].tail(3).mean()
            confidence = max(0.5, 1 - (recent_std / recent_mean)) if recent_mean > 0 else 0.5
        else:
            confidence = 0.5
        
        # Save prediction
        save_query = """
            INSERT INTO predictions (user_id, prediction_type, predicted_value, prediction_date, confidence_score)
            VALUES (%s, %s, %s, %s, %s)
        """
        next_month = (datetime.now().replace(day=1) + timedelta(days=32)).replace(day=1)
        DatabaseManager.execute_query(save_query, (
            user_id, 'monthly_expense', prediction, next_month.strftime('%Y-%m-%d'), confidence
        ))
        
        return jsonify({
            'success': True,
            'prediction': round(prediction, 2),
            'confidence': round(confidence * 100, 1),
            'message': f'Predicted expense for next month: ₹{prediction:,.2f}'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/api/predict/savings', methods=['POST'])
@token_required
def predict_savings():
    """Predict monthly savings"""
    try:
        user_id = session.get('user_id')
        
        # Get user transactions
        query = """
            SELECT date, transaction_type, amount
            FROM transactions
            WHERE user_id = %s
            ORDER BY date DESC
            LIMIT 500
        """
        transactions = DatabaseManager.execute_query(query, (user_id,), fetch=True)
        
        if not transactions:
            return jsonify({
                'success': False,
                'message': 'No transaction data available'
            })
        
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        
        # Calculate monthly income and expense
        df['year_month'] = df['date'].dt.to_period('M')
        monthly_summary = df.groupby(['year_month', 'transaction_type'])['amount'].sum().unstack(fill_value=0)
        
        if 'income' in monthly_summary.columns and 'expense' in monthly_summary.columns:
            monthly_summary['savings'] = monthly_summary['income'] - monthly_summary['expense']
            avg_savings = monthly_summary['savings'].mean()
            
            # Simple prediction: average of last 3 months
            if len(monthly_summary) >= 3:
                predicted_savings = monthly_summary['savings'].tail(3).mean()
            else:
                predicted_savings = avg_savings
            
            confidence = 0.75
        else:
            predicted_savings = 0
            confidence = 0.5
        
        # Save prediction
        save_query = """
            INSERT INTO predictions (user_id, prediction_type, predicted_value, prediction_date, confidence_score)
            VALUES (%s, %s, %s, %s, %s)
        """
        next_month = (datetime.now().replace(day=1) + timedelta(days=32)).replace(day=1)
        DatabaseManager.execute_query(save_query, (
            user_id, 'monthly_savings', predicted_savings, next_month.strftime('%Y-%m-%d'), confidence
        ))
        
        return jsonify({
            'success': True,
            'prediction': round(predicted_savings, 2),
            'confidence': round(confidence * 100, 1),
            'message': f'Predicted savings for next month: ₹{predicted_savings:,.2f}'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/api/predict/bills', methods=['POST'])
@token_required
def estimate_bills():
    """Estimate upcoming bills"""
    try:
        user_id = session.get('user_id')
        
        # Get bill transactions
        query = """
            SELECT date, amount, category
            FROM transactions
            WHERE user_id = %s AND category IN ('Bills', 'Rent')
            ORDER BY date DESC
            LIMIT 100
        """
        bills = DatabaseManager.execute_query(query, (user_id,), fetch=True)
        
        if not bills:
            return jsonify({
                'success': False,
                'message': 'No bill data available'
            })
        
        df = pd.DataFrame(bills)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        
        # Calculate average bills by category
        avg_bills = df.groupby('category')['amount'].mean()
        total_estimated = avg_bills.sum()
        
        bills_breakdown = {cat: round(amt, 2) for cat, amt in avg_bills.items()}
        
        return jsonify({
            'success': True,
            'total_estimated': round(total_estimated, 2),
            'breakdown': bills_breakdown,
            'message': f'Estimated upcoming bills: ₹{total_estimated:,.2f}'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/api/detect/anomalies', methods=['POST'])
@token_required
def detect_anomalies():
    """Detect anomalous transactions"""
    try:
        user_id = session.get('user_id')
        
        # Get recent transactions
        query = """
            SELECT date, amount, category, merchant
            FROM transactions
            WHERE user_id = %s AND transaction_type = 'expense'
            ORDER BY date DESC
            LIMIT 200
        """
        transactions = DatabaseManager.execute_query(query, (user_id,), fetch=True)
        
        if not transactions or len(transactions) < 10:
            return jsonify({
                'success': False,
                'message': 'Insufficient data for anomaly detection'
            })
        
        df = pd.DataFrame(transactions)
        df['amount'] = pd.to_numeric(df['amount'])
        
        anomalies = []
        
        # Detect anomalies by category
        for category in df['category'].unique():
            cat_data = df[df['category'] == category]['amount']
            
            if len(cat_data) < 5:
                continue
            
            mean = cat_data.mean()
            std = cat_data.std()
            
            # Find outliers (2.5 standard deviations)
            threshold = mean + (2.5 * std)
            outliers = df[(df['category'] == category) & (df['amount'] > threshold)]
            
            for _, row in outliers.head(3).iterrows():
                anomalies.append({
                    'date': row['date'].strftime('%Y-%m-%d') if hasattr(row['date'], 'strftime') else str(row['date']),
                    'amount': round(float(row['amount']), 2),
                    'category': row['category'],
                    'merchant': row['merchant'],
                    'reason': f'Amount significantly higher than average (₹{mean:.2f})'
                })
        
        return jsonify({
            'success': True,
            'anomalies': anomalies,
            'count': len(anomalies),
            'message': f'Found {len(anomalies)} unusual transactions'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/api/recommend/budget', methods=['POST'])
@token_required
def recommend_budget():
    """Recommend budget allocation"""
    try:
        user_id = session.get('user_id')
        
        # Get user expenses
        query = """
            SELECT category, SUM(amount) as total
            FROM transactions
            WHERE user_id = %s AND transaction_type = 'expense'
            GROUP BY category
        """
        expenses = DatabaseManager.execute_query(query, (user_id,), fetch=True)
        
        if not expenses:
            return jsonify({
                'success': False,
                'message': 'No expense data available'
            })
        
        df = pd.DataFrame(expenses)
        df['total'] = pd.to_numeric(df['total'])
        total_expense = df['total'].sum()
        
        # Calculate current percentages
        df['current_percentage'] = (df['total'] / total_expense * 100).round(1)
        
        # Recommended percentages (50/30/20 rule adapted)
        recommendations = {
            'Food': 15,
            'Rent': 30,
            'Bills': 10,
            'Travel': 10,
            'Shopping': 10,
            'Entertainment': 10,
            'Healthcare': 5,
            'Education': 5,
            'Other': 5
        }
        
        budget_recommendations = []
        for _, row in df.iterrows():
            category = row['category']
            current_pct = row['current_percentage']
            recommended_pct = recommendations.get(category, 5)
            recommended_amount = (total_expense * recommended_pct / 100)
            
            budget_recommendations.append({
                'category': category,
                'current_amount': round(float(row['total']), 2),
                'current_percentage': float(current_pct),
                'recommended_percentage': recommended_pct,
                'recommended_amount': round(recommended_amount, 2),
                'status': 'over' if current_pct > recommended_pct * 1.2 else 'under' if current_pct < recommended_pct * 0.8 else 'good'
            })
        
        return jsonify({
            'success': True,
            'recommendations': budget_recommendations,
            'total_expense': round(total_expense, 2),
            'message': 'Budget recommendations generated'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500