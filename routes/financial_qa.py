"""
Financial Q&A Routes - LLM-Powered Financial Assistant
Allows users to ask questions about their finances and get AI-powered answers
"""

from flask import Blueprint, request, jsonify, session
from functools import wraps
from utils.db_utils import DatabaseManager
import pandas as pd
from datetime import datetime, timedelta
import json

# Create Blueprint
financial_qa_bp = Blueprint('financial_qa', __name__)


def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Please login to access this feature'}), 401
        return f(*args, **kwargs)
    return decorated_function


@financial_qa_bp.route('/api/financial-qa/ask', methods=['POST'])
@login_required
def ask_financial_question():
    """
    Process user's financial question and provide AI-powered answer
    """
    try:
        user_id = session['user_id']
        question = request.json.get('question', '').strip()
        
        if not question:
            return jsonify({
                'success': False,
                'message': 'Please provide a question'
            }), 400
        
        # Get user's financial data
        financial_context = get_user_financial_context(user_id)
        
        # Process question and generate answer
        answer = process_financial_question(question, financial_context, user_id)
        
        # Save Q&A to history
        save_qa_history(user_id, question, answer)
        
        return jsonify({
            'success': True,
            'question': question,
            'answer': answer['response'],
            'insights': answer.get('insights', []),
            'suggestions': answer.get('suggestions', [])
        })
        
    except Exception as e:
        print(f"Error processing financial question: {e}")
        return jsonify({
            'success': False,
            'message': 'Error processing your question. Please try again.'
        }), 500


@financial_qa_bp.route('/api/financial-qa/history')
@login_required
def get_qa_history():
    """Get user's Q&A history"""
    try:
        user_id = session['user_id']
        
        query = """
            SELECT question, answer, created_at
            FROM financial_qa_history
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT 20
        """
        
        history = DatabaseManager.execute_query(query, (user_id,), fetch=True)
        
        return jsonify({
            'success': True,
            'history': history or []
        })
        
    except Exception as e:
        print(f"Error fetching Q&A history: {e}")
        return jsonify({
            'success': False,
            'message': 'Error loading history'
        }), 500


def get_user_financial_context(user_id):
    """Get comprehensive financial context for the user"""
    context = {
        'transactions': [],
        'goals': [],
        'summary': {}
    }
    
    try:
        # Get recent transactions
        trans_query = """
            SELECT date, transaction_type, amount, category, merchant
            FROM transactions
            WHERE user_id = %s
            ORDER BY date DESC
            LIMIT 100
        """
        transactions = DatabaseManager.execute_query(trans_query, (user_id,), fetch=True)
        context['transactions'] = transactions or []
        
        # Get goals
        goals_query = """
            SELECT goal_name, goal_type, target_amount, current_amount, 
                   target_date, status, priority
            FROM goals
            WHERE user_id = %s AND status = 'active'
        """
        goals = DatabaseManager.execute_query(goals_query, (user_id,), fetch=True)
        context['goals'] = goals or []
        
        # Calculate summary statistics
        if transactions:
            df = pd.DataFrame(transactions)
            df['amount'] = pd.to_numeric(df['amount'])
            
            total_income = df[df['transaction_type'] == 'income']['amount'].sum()
            total_expense = df[df['transaction_type'] == 'expense']['amount'].sum()
            
            # Current month
            current_month = datetime.now().replace(day=1)
            df['date'] = pd.to_datetime(df['date'])
            current_month_data = df[df['date'] >= current_month]
            
            month_income = current_month_data[current_month_data['transaction_type'] == 'income']['amount'].sum()
            month_expense = current_month_data[current_month_data['transaction_type'] == 'expense']['amount'].sum()
            
            # Category breakdown
            category_spending = df[df['transaction_type'] == 'expense'].groupby('category')['amount'].sum().to_dict()
            
            context['summary'] = {
                'total_income': float(total_income),
                'total_expense': float(total_expense),
                'total_savings': float(total_income - total_expense),
                'month_income': float(month_income),
                'month_expense': float(month_expense),
                'month_savings': float(month_income - month_expense),
                'category_spending': category_spending,
                'avg_daily_expense': float(total_expense / 30) if total_expense > 0 else 0
            }
    
    except Exception as e:
        print(f"Error getting financial context: {e}")
    
    return context


def process_financial_question(question, context, user_id):
    """
    Process the financial question and generate an intelligent answer
    """
    question_lower = question.lower()
    
    # Detect question type and generate appropriate response
    if any(word in question_lower for word in ['why', 'higher', 'more', 'increased', 'expense']):
        return analyze_expense_increase(question, context)
    
    elif any(word in question_lower for word in ['afford', 'can i buy', 'purchase', 'bike', 'car']):
        return analyze_affordability(question, context)
    
    elif any(word in question_lower for word in ['save', 'saving', 'how to save', 'reduce']):
        return provide_saving_suggestions(question, context)
    
    elif any(word in question_lower for word in ['budget', 'spending', 'category']):
        return analyze_spending_patterns(question, context)
    
    elif any(word in question_lower for word in ['goal', 'target', 'achieve']):
        return analyze_goals(question, context)
    
    else:
        return provide_general_financial_advice(question, context)


def analyze_expense_increase(question, context):
    """Analyze why expenses are higher"""
    summary = context['summary']
    category_spending = summary.get('category_spending', {})
    
    # Find top spending categories
    top_categories = sorted(category_spending.items(), key=lambda x: x[1], reverse=True)[:3]
    
    response = f"Based on your recent transactions:\n\n"
    response += f"💰 This month's expenses: ₹{summary['month_expense']:,.0f}\n"
    response += f"📊 Average daily spending: ₹{summary['avg_daily_expense']:,.0f}\n\n"
    
    response += "🔍 Top spending categories:\n"
    for cat, amount in top_categories:
        percentage = (amount / summary['total_expense'] * 100) if summary['total_expense'] > 0 else 0
        response += f"   • {cat}: ₹{amount:,.0f} ({percentage:.1f}%)\n"
    
    insights = [
        f"Your highest expense category is {top_categories[0][0]} with ₹{top_categories[0][1]:,.0f}",
        f"Monthly expenses are {'higher' if summary['month_expense'] > summary['avg_daily_expense'] * 30 else 'lower'} than average"
    ]
    
    suggestions = [
        f"Consider reducing {top_categories[0][0]} expenses by 10-15%",
        "Track daily expenses to identify unnecessary spending",
        "Set category-wise budget limits"
    ]
    
    return {
        'response': response,
        'insights': insights,
        'suggestions': suggestions
    }


def analyze_affordability(question, context):
    """Analyze if user can afford a purchase"""
    import re
    
    # Extract amount from question
    amount_match = re.search(r'₹?\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:l|lakh|lakhs|k|thousand)?', question.lower())
    
    if amount_match:
        amount_str = amount_match.group(1).replace(',', '')
        multiplier = 1
        
        if 'l' in question.lower() or 'lakh' in question.lower():
            multiplier = 100000
        elif 'k' in question.lower() or 'thousand' in question.lower():
            multiplier = 1000
        
        target_amount = float(amount_str) * multiplier
    else:
        target_amount = 150000  # Default assumption
    
    summary = context['summary']
    current_savings = summary['total_savings']
    monthly_savings = summary['month_savings']
    
    response = f"💡 Affordability Analysis for ₹{target_amount:,.0f}:\n\n"
    
    if current_savings >= target_amount:
        response += f"✅ Great news! You have ₹{current_savings:,.0f} in savings.\n"
        response += f"You can afford this purchase right now!\n\n"
        remaining = current_savings - target_amount
        response += f"💰 Remaining savings after purchase: ₹{remaining:,.0f}\n"
        
        insights = ["You have sufficient savings for this purchase"]
        suggestions = [
            "Consider keeping an emergency fund of 3-6 months expenses",
            "Ensure this purchase aligns with your financial goals"
        ]
    else:
        shortfall = target_amount - current_savings
        months_needed = (shortfall / monthly_savings) if monthly_savings > 0 else float('inf')
        
        response += f"📊 Current savings: ₹{current_savings:,.0f}\n"
        response += f"💸 Amount needed: ₹{shortfall:,.0f}\n"
        response += f"📅 Monthly savings: ₹{monthly_savings:,.0f}\n\n"
        
        if months_needed < float('inf'):
            response += f"⏰ You can afford this in approximately {int(months_needed)} months\n"
            response += f"   if you maintain current savings rate.\n"
        else:
            response += f"⚠️ You need to start saving to afford this purchase.\n"
        
        insights = [
            f"You need ₹{shortfall:,.0f} more to afford this",
            f"Current monthly savings: ₹{monthly_savings:,.0f}"
        ]
        
        suggestions = [
            f"Save ₹{shortfall/6:,.0f} per month for 6 months",
            "Reduce non-essential expenses to increase savings",
            "Consider creating a dedicated goal for this purchase"
        ]
    
    return {
        'response': response,
        'insights': insights,
        'suggestions': suggestions
    }


def provide_saving_suggestions(question, context):
    """Provide personalized saving suggestions"""
    summary = context['summary']
    category_spending = summary.get('category_spending', {})
    
    response = "💡 Personalized Saving Strategies:\n\n"
    
    # Analyze spending patterns
    top_categories = sorted(category_spending.items(), key=lambda x: x[1], reverse=True)
    
    suggestions = []
    
    # Category-specific suggestions
    for cat, amount in top_categories[:3]:
        if cat.lower() in ['food', 'dining', 'restaurant']:
            suggestions.append(f"🍽️ {cat}: Cook at home more often - potential savings: ₹{amount * 0.3:,.0f}/month")
        elif cat.lower() in ['shopping', 'clothes', 'fashion']:
            suggestions.append(f"🛍️ {cat}: Buy only essentials - potential savings: ₹{amount * 0.4:,.0f}/month")
        elif cat.lower() in ['entertainment', 'movies', 'streaming']:
            suggestions.append(f"🎬 {cat}: Reduce subscriptions - potential savings: ₹{amount * 0.5:,.0f}/month")
        elif cat.lower() in ['travel', 'transport', 'fuel']:
            suggestions.append(f"🚗 {cat}: Use public transport - potential savings: ₹{amount * 0.25:,.0f}/month")
    
    # Calculate potential total savings
    potential_savings = sum([amount * 0.3 for _, amount in top_categories[:3]])
    
    response += f"📊 Current monthly expenses: ₹{summary['month_expense']:,.0f}\n"
    response += f"💰 Potential monthly savings: ₹{potential_savings:,.0f}\n\n"
    response += "🎯 Actionable Steps:\n"
    
    for i, suggestion in enumerate(suggestions[:5], 1):
        response += f"   {i}. {suggestion}\n"
    
    insights = [
        f"You can potentially save ₹{potential_savings:,.0f} per month",
        f"Focus on reducing {top_categories[0][0]} expenses first"
    ]
    
    general_suggestions = [
        "Create a monthly budget and stick to it",
        "Use the 50/30/20 rule: 50% needs, 30% wants, 20% savings",
        "Automate savings by setting up recurring transfers",
        "Track every expense to identify spending leaks"
    ]
    
    return {
        'response': response,
        'insights': insights,
        'suggestions': general_suggestions
    }


def analyze_spending_patterns(question, context):
    """Analyze spending patterns"""
    summary = context['summary']
    category_spending = summary.get('category_spending', {})
    
    response = "📊 Your Spending Pattern Analysis:\n\n"
    
    total_expense = summary['total_expense']
    
    response += f"💸 Total expenses: ₹{total_expense:,.0f}\n"
    response += f"📅 Monthly average: ₹{summary['month_expense']:,.0f}\n\n"
    
    response += "📈 Category Breakdown:\n"
    for cat, amount in sorted(category_spending.items(), key=lambda x: x[1], reverse=True):
        percentage = (amount / total_expense * 100) if total_expense > 0 else 0
        response += f"   • {cat}: ₹{amount:,.0f} ({percentage:.1f}%)\n"
    
    insights = [
        f"Highest spending: {max(category_spending.items(), key=lambda x: x[1])[0]}",
        f"Average daily expense: ₹{summary['avg_daily_expense']:,.0f}"
    ]
    
    suggestions = [
        "Set category-wise budget limits",
        "Review and reduce top 3 expense categories",
        "Use expense tracking apps for better visibility"
    ]
    
    return {
        'response': response,
        'insights': insights,
        'suggestions': suggestions
    }


def analyze_goals(question, context):
    """Analyze financial goals"""
    goals = context['goals']
    
    if not goals:
        response = "🎯 You haven't set any financial goals yet!\n\n"
        response += "Setting goals is crucial for financial success. Consider creating goals for:\n"
        response += "   • Emergency fund (3-6 months expenses)\n"
        response += "   • Major purchases (car, house, etc.)\n"
        response += "   • Debt payoff\n"
        response += "   • Investment targets\n"
        
        return {
            'response': response,
            'insights': ["No active goals found"],
            'suggestions': ["Create your first financial goal", "Start with an emergency fund goal"]
        }
    
    response = f"🎯 Your Financial Goals ({len(goals)} active):\n\n"
    
    for goal in goals:
        progress = (float(goal['current_amount']) / float(goal['target_amount']) * 100) if float(goal['target_amount']) > 0 else 0
        remaining = float(goal['target_amount']) - float(goal['current_amount'])
        
        response += f"📌 {goal['goal_name']}\n"
        response += f"   Target: ₹{float(goal['target_amount']):,.0f}\n"
        response += f"   Progress: {progress:.1f}% (₹{float(goal['current_amount']):,.0f})\n"
        response += f"   Remaining: ₹{remaining:,.0f}\n"
        response += f"   Deadline: {goal['target_date']}\n\n"
    
    insights = [
        f"You have {len(goals)} active goals",
        f"Total target amount: ₹{sum([float(g['target_amount']) for g in goals]):,.0f}"
    ]
    
    suggestions = [
        "Prioritize high-priority goals",
        "Make regular contributions to stay on track",
        "Review and adjust goals quarterly"
    ]
    
    return {
        'response': response,
        'insights': insights,
        'suggestions': suggestions
    }


def provide_general_financial_advice(question, context):
    """Provide general financial advice"""
    summary = context['summary']
    
    response = "💡 Financial Overview & Advice:\n\n"
    response += f"💰 Total Income: ₹{summary['total_income']:,.0f}\n"
    response += f"💸 Total Expenses: ₹{summary['total_expense']:,.0f}\n"
    response += f"💵 Total Savings: ₹{summary['total_savings']:,.0f}\n"
    
    savings_rate = (summary['total_savings'] / summary['total_income'] * 100) if summary['total_income'] > 0 else 0
    response += f"📊 Savings Rate: {savings_rate:.1f}%\n\n"
    
    if savings_rate < 20:
        response += "⚠️ Your savings rate is below recommended 20%. Focus on increasing savings.\n"
    elif savings_rate < 30:
        response += "✅ Good savings rate! Try to push it to 30% for better financial security.\n"
    else:
        response += "🌟 Excellent savings rate! You're on track for strong financial health.\n"
    
    insights = [
        f"Savings rate: {savings_rate:.1f}%",
        f"Monthly savings: ₹{summary['month_savings']:,.0f}"
    ]
    
    suggestions = [
        "Build an emergency fund of 6 months expenses",
        "Start investing in diversified portfolios",
        "Review insurance coverage (health, life, term)",
        "Create a retirement savings plan",
        "Minimize high-interest debt"
    ]
    
    return {
        'response': response,
        'insights': insights,
        'suggestions': suggestions
    }


def save_qa_history(user_id, question, answer):
    """Save Q&A to history"""
    try:
        # First check if table exists, if not create it
        create_table_query = """
            CREATE TABLE IF NOT EXISTS financial_qa_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_user_date (user_id, created_at)
            )
        """
        DatabaseManager.execute_query(create_table_query)
        
        # Save the Q&A
        insert_query = """
            INSERT INTO financial_qa_history (user_id, question, answer)
            VALUES (%s, %s, %s)
        """
        DatabaseManager.execute_query(
            insert_query,
            (user_id, question, json.dumps(answer))
        )
    except Exception as e:
        print(f"Error saving Q&A history: {e}")