from flask import Blueprint, render_template, session, jsonify, request
from routes.auth import token_required
from utils.db_utils import DatabaseManager
from utils.ai_suggestions import AISuggestionEngine
import pandas as pd
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@token_required
def dashboard_page():
    """Main dashboard page"""
    user_id = session.get('user_id')
    username = session.get('username')
    
    # Get user statistics
    stats = get_user_statistics(user_id)
    
    # Generate AI suggestions
    AISuggestionEngine.generate_suggestions(user_id)
    
    # Get recent suggestions from database
    suggestion_query = """
        SELECT suggestion_text, suggestion_type, category, priority, created_at
        FROM ai_suggestions
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 10
    """
    db_suggestions = DatabaseManager.execute_query(suggestion_query, (user_id,), fetch=True)
    
    return render_template('dashboard.html', 
                         username=username,
                         stats=stats,
                         suggestions=db_suggestions)

@dashboard_bp.route('/goals')
@token_required
def goals_page():
    """Financial goals page"""
    return render_template('goals.html')

@dashboard_bp.route('/financial-qa')
@token_required
def financial_qa_page():
    """Financial Q&A page"""
    return render_template('financial_qa.html')

@dashboard_bp.route('/api/dashboard/data')
@token_required
def get_dashboard_data():
    """Get dashboard data for visualizations"""
    user_id = session.get('user_id')
    
    query = """
        SELECT date, transaction_type, amount, category, merchant
        FROM transactions
        WHERE user_id = %s
        ORDER BY date DESC
        LIMIT 1000
    """
    transactions = DatabaseManager.execute_query(query, (user_id,), fetch=True)
    
    if not transactions:
        return jsonify({
            'monthly_expenses': [], 'category_spending': [], 
            'income_vs_expense': [], 'spending_distribution': []
        })
    
    df = pd.DataFrame(transactions)
    df['date'] = pd.to_datetime(df['date'])
    df['amount'] = pd.to_numeric(df['amount'])
    
    # Monthly expenses
    monthly_expenses = df[df['transaction_type']=='expense'].groupby(
        df['date'].dt.to_period('M')
    )['amount'].sum().reset_index()
    monthly_expenses['date'] = monthly_expenses['date'].dt.to_timestamp()
    
    # Category-wise spending
    category_spending = df[df['transaction_type']=='expense'].groupby('category')['amount'].sum().reset_index()
    category_spending = category_spending.sort_values('amount', ascending=False)
    
    # Income vs expense
    income_expense = df.groupby([df['date'].dt.to_period('M'), 'transaction_type'])['amount'].sum().reset_index()
    income_expense['date'] = income_expense['date'].dt.to_timestamp()
    
    income_data = income_expense[income_expense['transaction_type']=='income']
    expense_data = income_expense[income_expense['transaction_type']=='expense']
    
    # Spending distribution
    expenses = df[df['transaction_type']=='expense']['amount']
    bins = [0, 500, 1000, 2000, 5000, 10000, 50000]
    labels = ['0-500', '500-1K', '1K-2K', '2K-5K', '5K-10K', '10K+']
    distribution = pd.cut(expenses, bins=bins, labels=labels).value_counts().sort_index()
    
    return jsonify({
        'monthly_expenses': {
            'labels': monthly_expenses['date'].dt.strftime('%b %Y').tolist(),
            'values': monthly_expenses['amount'].tolist()
        },
        'category_spending': {
            'labels': category_spending['category'].tolist(),
            'values': category_spending['amount'].tolist()
        },
        'income_vs_expense': {
            'labels': income_data['date'].dt.strftime('%b %Y').tolist(),
            'income': income_data['amount'].tolist(),
            'expense': expense_data['amount'].tolist()
        },
        'spending_distribution': {
            'labels': distribution.index.tolist(),
            'values': distribution.values.tolist()
        }
    })

def get_user_statistics(user_id):
    """Get user statistics for dashboard"""
    count_query = "SELECT COUNT(*) as count FROM transactions WHERE user_id = %s"
    count_result = DatabaseManager.execute_query(count_query, (user_id,), fetch=True)
    total_transactions = count_result[0]['count'] if count_result else 0
    
    sum_query = """
        SELECT transaction_type, SUM(amount) as total
        FROM transactions
        WHERE user_id = %s
        GROUP BY transaction_type
    """
    sums = DatabaseManager.execute_query(sum_query, (user_id,), fetch=True)
    
    total_income = 0
    total_expense = 0
    for row in sums:
        if row['transaction_type'] == 'income':
            total_income = float(row['total'])
        elif row['transaction_type'] == 'expense':
            total_expense = float(row['total'])
    
    current_month = datetime.now().replace(day=1).strftime('%Y-%m-%d')
    month_query = """
        SELECT SUM(amount) as total
        FROM transactions
        WHERE user_id = %s AND transaction_type='expense' AND date >= %s
    """
    month_result = DatabaseManager.execute_query(month_query, (user_id, current_month), fetch=True)
    current_month_expense = float(month_result[0]['total']) if month_result and month_result[0]['total'] else 0
    
    total_savings = total_income - total_expense
    savings_rate = (total_savings / total_income * 100) if total_income>0 else 0
    
    return {
        'total_transactions': total_transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'total_savings': total_savings,
        'savings_rate': savings_rate,
        'current_month_expense': current_month_expense
    }

# ----------------- CLEAR DATA ROUTE -----------------
@dashboard_bp.route('/api/dashboard/clear', methods=['POST'])
@token_required
def clear_dashboard_data():
    """Clear all transactions and AI suggestions for a user"""
    user_id = session.get('user_id')
    try:
        DatabaseManager.execute_query("DELETE FROM transactions WHERE user_id=%s", (user_id,))
        DatabaseManager.execute_query("DELETE FROM ai_suggestions WHERE user_id=%s", (user_id,))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})