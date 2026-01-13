"""
Goals Routes - Financial Goal Setting and Tracking
Integrated with Dashboard
"""

from flask import Blueprint, request, jsonify, session
from functools import wraps
from datetime import datetime, timedelta
from decimal import Decimal
from utils.db_utils import DatabaseManager

# Create Blueprint
goals_bp = Blueprint('goals', __name__)


def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Please login to access this feature'}), 401
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# API ENDPOINTS FOR DASHBOARD INTEGRATION
# ============================================================================

@goals_bp.route('/api/goals/list')
@login_required
def get_goals_list():
    """Get all goals for the current user"""
    try:
        user_id = session['user_id']
        
        # Get all goals with progress
        query = """
            SELECT g.*, 
                   COALESCE(SUM(gc.amount), 0) as total_contributed,
                   ROUND((COALESCE(SUM(gc.amount), 0) / g.target_amount) * 100, 2) as progress_percentage,
                   DATEDIFF(g.target_date, CURDATE()) as days_remaining
            FROM goals g
            LEFT JOIN goal_contributions gc ON g.id = gc.goal_id
            WHERE g.user_id = %s
            GROUP BY g.id
            ORDER BY g.status ASC, g.priority DESC, g.target_date ASC
        """
        
        goals = DatabaseManager.execute_query(query, (user_id,), fetch=True)
        
        # Get statistics
        stats_query = """
            SELECT 
                COUNT(*) as total_goals,
                SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active_goals,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_goals,
                SUM(CASE WHEN status = 'active' THEN target_amount ELSE 0 END) as total_target,
                SUM(CASE WHEN status = 'active' THEN current_amount ELSE 0 END) as total_saved
            FROM goals
            WHERE user_id = %s
        """
        
        stats = DatabaseManager.execute_query(stats_query, (user_id,), fetch=True)
        stats_data = stats[0] if stats else {
            'total_goals': 0,
            'active_goals': 0,
            'completed_goals': 0,
            'total_target': 0,
            'total_saved': 0
        }
        
        return jsonify({
            'success': True,
            'goals': goals,
            'stats': stats_data
        })
        
    except Exception as e:
        print(f"Error loading goals: {e}")
        return jsonify({'success': False, 'message': 'Error loading goals'}), 500


@goals_bp.route('/api/goals/create', methods=['POST'])
@login_required
def create_goal():
    """Create a new financial goal"""
    try:
        user_id = session['user_id']
        
        # Get form data
        goal_name = request.form.get('goal_name')
        goal_type = request.form.get('goal_type')
        target_amount = float(request.form.get('target_amount'))
        target_date = request.form.get('target_date')
        category = request.form.get('category', '')
        description = request.form.get('description', '')
        priority = request.form.get('priority', 'medium')
        
        # Validation
        if not all([goal_name, goal_type, target_amount, target_date]):
            return jsonify({
                'success': False,
                'message': 'Please fill in all required fields'
            }), 400
        
        if target_amount <= 0:
            return jsonify({
                'success': False,
                'message': 'Target amount must be positive'
            }), 400
        
        # Validate target date is in future
        target_dt = datetime.strptime(target_date, '%Y-%m-%d').date()
        if target_dt <= datetime.now().date():
            return jsonify({
                'success': False,
                'message': 'Target date must be in the future'
            }), 400
        
        # Insert goal
        insert_query = """
            INSERT INTO goals 
            (user_id, goal_name, goal_type, target_amount, start_date, target_date, 
             category, description, priority)
            VALUES (%s, %s, %s, %s, CURDATE(), %s, %s, %s, %s)
        """
        
        DatabaseManager.execute_query(
            insert_query,
            (user_id, goal_name, goal_type, target_amount, target_date, 
             category, description, priority)
        )
        
        return jsonify({
            'success': True,
            'message': f'Goal "{goal_name}" created successfully!'
        })
        
    except Exception as e:
        print(f"Error creating goal: {e}")
        return jsonify({
            'success': False,
            'message': 'Error creating goal. Please try again.'
        }), 500


@goals_bp.route('/api/goals/<int:goal_id>/contribute', methods=['POST'])
@login_required
def add_contribution(goal_id):
    """Add contribution to a goal"""
    try:
        user_id = session['user_id']
        
        amount = float(request.form.get('amount'))
        contribution_date = request.form.get('contribution_date', datetime.now().date())
        notes = request.form.get('notes', '')
        
        if amount <= 0:
            return jsonify({
                'success': False,
                'message': 'Amount must be positive'
            }), 400
        
        # Verify goal ownership
        verify_query = "SELECT * FROM goals WHERE id = %s AND user_id = %s"
        goal = DatabaseManager.execute_query(verify_query, (goal_id, user_id), fetch=True)
        
        if not goal:
            return jsonify({
                'success': False,
                'message': 'Goal not found'
            }), 404
        
        goal_data = goal[0]
        
        # Add contribution
        contrib_query = """
            INSERT INTO goal_contributions (goal_id, amount, contribution_date, notes)
            VALUES (%s, %s, %s, %s)
        """
        
        DatabaseManager.execute_query(
            contrib_query,
            (goal_id, amount, contribution_date, notes)
        )
        
        # Update goal current amount
        update_query = """
            UPDATE goals 
            SET current_amount = current_amount + %s
            WHERE id = %s
        """
        
        DatabaseManager.execute_query(update_query, (amount, goal_id))
        
        # Check if goal is completed
        new_amount = float(goal_data['current_amount']) + amount
        if new_amount >= float(goal_data['target_amount']):
            complete_query = "UPDATE goals SET status = 'completed' WHERE id = %s"
            DatabaseManager.execute_query(complete_query, (goal_id,))
        
        return jsonify({
            'success': True,
            'message': 'Contribution added successfully'
        })
        
    except Exception as e:
        print(f"Error adding contribution: {e}")
        return jsonify({
            'success': False,
            'message': 'Error adding contribution'
        }), 500


@goals_bp.route('/api/goals/<int:goal_id>/details')
@login_required
def get_goal_details(goal_id):
    """Get detailed goal information"""
    try:
        user_id = session['user_id']
        
        # Get goal details
        goal_query = """
            SELECT g.*,
                   COALESCE(SUM(gc.amount), 0) as total_contributed,
                   ROUND((COALESCE(SUM(gc.amount), 0) / g.target_amount) * 100, 2) as progress_percentage,
                   DATEDIFF(g.target_date, CURDATE()) as days_remaining,
                   DATEDIFF(CURDATE(), g.start_date) as days_elapsed
            FROM goals g
            LEFT JOIN goal_contributions gc ON g.id = gc.goal_id
            WHERE g.id = %s AND g.user_id = %s
            GROUP BY g.id
        """
        
        goal = DatabaseManager.execute_query(goal_query, (goal_id, user_id), fetch=True)
        
        if not goal:
            return jsonify({
                'success': False,
                'message': 'Goal not found'
            }), 404
        
        goal_data = goal[0]
        
        # Get contributions history
        contrib_query = """
            SELECT * FROM goal_contributions
            WHERE goal_id = %s
            ORDER BY contribution_date DESC
            LIMIT 10
        """
        
        contributions = DatabaseManager.execute_query(contrib_query, (goal_id,), fetch=True)
        
        # Calculate AI recommendations
        recommendations = calculate_goal_recommendations(goal_data, contributions)
        
        return jsonify({
            'success': True,
            'goal': goal_data,
            'contributions': contributions,
            'recommendations': recommendations
        })
        
    except Exception as e:
        print(f"Error loading goal details: {e}")
        return jsonify({
            'success': False,
            'message': 'Error loading goal details'
        }), 500


@goals_bp.route('/api/goals/<int:goal_id>/update', methods=['POST'])
@login_required
def update_goal(goal_id):
    """Update goal details"""
    try:
        user_id = session['user_id']
        
        # Verify ownership
        verify_query = "SELECT id FROM goals WHERE id = %s AND user_id = %s"
        goal = DatabaseManager.execute_query(verify_query, (goal_id, user_id), fetch=True)
        
        if not goal:
            return jsonify({
                'success': False,
                'message': 'Goal not found'
            }), 404
        
        # Get update fields
        updates = []
        values = []
        
        if 'goal_name' in request.form:
            updates.append("goal_name = %s")
            values.append(request.form['goal_name'])
        
        if 'target_amount' in request.form:
            updates.append("target_amount = %s")
            values.append(float(request.form['target_amount']))
        
        if 'target_date' in request.form:
            updates.append("target_date = %s")
            values.append(request.form['target_date'])
        
        if 'priority' in request.form:
            updates.append("priority = %s")
            values.append(request.form['priority'])
        
        if 'status' in request.form:
            updates.append("status = %s")
            values.append(request.form['status'])
        
        if 'description' in request.form:
            updates.append("description = %s")
            values.append(request.form['description'])
        
        if 'category' in request.form:
            updates.append("category = %s")
            values.append(request.form['category'])
        
        if 'goal_type' in request.form:
            updates.append("goal_type = %s")
            values.append(request.form['goal_type'])
        
        if updates:
            values.append(goal_id)
            query = f"UPDATE goals SET {', '.join(updates)} WHERE id = %s"
            DatabaseManager.execute_query(query, tuple(values))
        
        return jsonify({
            'success': True,
            'message': 'Goal updated successfully'
        })
        
    except Exception as e:
        print(f"Error updating goal: {e}")
        return jsonify({
            'success': False,
            'message': 'Error updating goal'
        }), 500


@goals_bp.route('/api/goals/<int:goal_id>/delete', methods=['POST'])
@login_required
def delete_goal(goal_id):
    """Delete a goal"""
    try:
        user_id = session['user_id']
        
        # Verify ownership and delete
        delete_query = """
            DELETE FROM goals 
            WHERE id = %s AND user_id = %s
        """
        
        DatabaseManager.execute_query(delete_query, (goal_id, user_id))
        
        return jsonify({
            'success': True,
            'message': 'Goal deleted successfully'
        })
        
    except Exception as e:
        print(f"Error deleting goal: {e}")
        return jsonify({
            'success': False,
            'message': 'Error deleting goal'
        }), 500


@goals_bp.route('/api/goals/stats')
@login_required
def get_goals_stats():
    """Get overall goals statistics for dashboard"""
    try:
        user_id = session['user_id']
        
        stats_query = """
            SELECT 
                COUNT(*) as total_goals,
                SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active_goals,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_goals,
                SUM(target_amount) as total_target,
                SUM(current_amount) as total_saved,
                ROUND(AVG(CASE WHEN status = 'active' 
                    THEN (current_amount / target_amount * 100) 
                    ELSE NULL END), 2) as avg_progress
            FROM goals
            WHERE user_id = %s
        """
        
        stats = DatabaseManager.execute_query(stats_query, (user_id,), fetch=True)
        stats_data = stats[0] if stats else {}
        
        # Get goal types distribution
        types_query = """
            SELECT 
                goal_type,
                COUNT(*) as count,
                SUM(target_amount) as total_amount
            FROM goals
            WHERE user_id = %s AND status = 'active'
            GROUP BY goal_type
        """
        
        goal_types = DatabaseManager.execute_query(types_query, (user_id,), fetch=True)
        
        return jsonify({
            'success': True,
            'stats': stats_data,
            'goal_types': goal_types
        })
        
    except Exception as e:
        print(f"Error getting goals stats: {e}")
        return jsonify({
            'success': False,
            'message': 'Error loading statistics'
        }), 500


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_goal_recommendations(goal, contributions):
    """Calculate AI-powered recommendations for goal achievement"""
    recommendations = {
        'monthly_contribution': 0,
        'projected_completion': None,
        'on_track': False,
        'suggestions': []
    }
    
    try:
        target_amount = float(goal['target_amount'])
        current_amount = float(goal.get('total_contributed', 0))
        remaining_amount = target_amount - current_amount
        
        days_remaining = goal.get('days_remaining', 0)
        
        if days_remaining > 0 and remaining_amount > 0:
            # Calculate required monthly contribution
            months_remaining = days_remaining / 30
            recommendations['monthly_contribution'] = remaining_amount / months_remaining if months_remaining > 0 else remaining_amount
            
            # Calculate average contribution and projected completion
            if contributions and len(contributions) > 0:
                total_days = goal.get('days_elapsed', 1)
                if total_days > 0:
                    avg_daily_contribution = current_amount / total_days
                    if avg_daily_contribution > 0:
                        projected_days = remaining_amount / avg_daily_contribution
                        projected_date = datetime.now() + timedelta(days=projected_days)
                        recommendations['projected_completion'] = projected_date.strftime('%Y-%m-%d')
                        
                        # Check if on track
                        expected_progress = (total_days / (total_days + days_remaining)) * 100
                        actual_progress = (current_amount / target_amount) * 100
                        recommendations['on_track'] = actual_progress >= (expected_progress - 10)
            
            # Generate suggestions based on progress
            monthly_req = recommendations['monthly_contribution']
            
            if monthly_req > 0:
                if monthly_req < 1000:
                    recommendations['suggestions'].append("Great! You're close to your goal. Keep it up!")
                elif monthly_req < 5000:
                    recommendations['suggestions'].append(f"Save ₹{monthly_req:.0f}/month to reach your goal on time")
                elif monthly_req < 10000:
                    recommendations['suggestions'].append(f"Try to save ₹{monthly_req:.0f}/month. Consider cutting non-essential expenses.")
                else:
                    recommendations['suggestions'].append("Consider extending your deadline or adjusting the target amount")
            
            # Add status-based suggestions
            if not recommendations['on_track'] and contributions:
                recommendations['suggestions'].append("You're falling behind schedule. Try to increase your contributions.")
            elif recommendations['on_track']:
                recommendations['suggestions'].append("Excellent progress! You're on track to meet your goal.")
            
            # Deadline-based suggestions
            if days_remaining < 30:
                recommendations['suggestions'].append("⚠️ Goal deadline is approaching soon. Stay focused!")
            elif days_remaining < 90:
                recommendations['suggestions'].append("📅 Less than 3 months remaining. Time to prioritize this goal!")
            
            # Initial contribution suggestion
            if current_amount == 0:
                recommendations['suggestions'].append("🚀 Start contributing today to build momentum!")
            
            # Small wins celebration
            progress_pct = (current_amount / target_amount) * 100
            if progress_pct >= 25 and progress_pct < 26:
                recommendations['suggestions'].append("🎉 You've reached 25% of your goal!")
            elif progress_pct >= 50 and progress_pct < 51:
                recommendations['suggestions'].append("🎉 Halfway there! Keep up the great work!")
            elif progress_pct >= 75 and progress_pct < 76:
                recommendations['suggestions'].append("🎉 75% complete! The finish line is in sight!")
        
        elif remaining_amount <= 0:
            recommendations['suggestions'].append("🎉 Congratulations! You've achieved your goal!")
        
    except Exception as e:
        print(f"Error calculating recommendations: {e}")
        recommendations['suggestions'].append("Unable to calculate recommendations at this time.")
    
    return recommendations


def generate_goal_suggestions_for_user(user_id):
    """
    Generate goal-related suggestions for AI Suggestions Engine
    This function can be called from your AISuggestionEngine
    """
    suggestions = []
    
    try:
        # Get user's active goals
        goals_query = """
            SELECT g.*,
                   COALESCE(SUM(gc.amount), 0) as total_contributed,
                   DATEDIFF(g.target_date, CURDATE()) as days_remaining
            FROM goals g
            LEFT JOIN goal_contributions gc ON g.id = gc.goal_id
            WHERE g.user_id = %s AND g.status = 'active'
            GROUP BY g.id
        """
        
        goals = DatabaseManager.execute_query(goals_query, (user_id,), fetch=True)
        
        if not goals or len(goals) == 0:
            # Suggest creating a goal
            suggestions.append({
                'text': "💡 Start your financial journey by setting a goal! Whether it's an emergency fund, vacation, or a big purchase - having clear goals helps you save better.",
                'type': 'goal_suggestion',
                'category': 'Goals',
                'priority': 'medium'
            })
            return suggestions
        
        for goal in goals:
            target_amount = float(goal['target_amount'])
            current_amount = float(goal['total_contributed'])
            remaining = target_amount - current_amount
            days_remaining = goal['days_remaining']
            
            # Progress-based suggestions
            progress_pct = (current_amount / target_amount) * 100 if target_amount > 0 else 0
            
            # Behind schedule warning
            if days_remaining > 0:
                expected_progress = ((goal.get('days_elapsed', 0) or 1) / 
                                   ((goal.get('days_elapsed', 0) or 1) + days_remaining)) * 100
                
                if progress_pct < expected_progress - 15:
                    monthly_needed = (remaining / (days_remaining / 30)) if days_remaining > 0 else 0
                    suggestions.append({
                        'text': f"⚠️ Your '{goal['goal_name']}' goal is behind schedule. Try saving ₹{monthly_needed:.0f}/month to catch up.",
                        'type': 'goal_suggestion',
                        'category': 'Goals',
                        'priority': 'high'
                    })
            
            # Upcoming deadline warnings
            if 0 < days_remaining <= 30:
                suggestions.append({
                    'text': f"⏰ Your '{goal['goal_name']}' goal is due in {days_remaining} days! You need ₹{remaining:.0f} more to reach it.",
                    'type': 'goal_suggestion',
                    'category': 'Goals',
                    'priority': 'high'
                })
            elif 30 < days_remaining <= 90:
                suggestions.append({
                    'text': f"📅 Your '{goal['goal_name']}' goal is due in {days_remaining} days. You're {progress_pct:.0f}% there!",
                    'type': 'goal_suggestion',
                    'category': 'Goals',
                    'priority': 'medium'
                })
            
            # Milestone celebrations
            if 24 <= progress_pct < 26:
                suggestions.append({
                    'text': f"🎉 You're 25% done with your '{goal['goal_name']}' goal! Keep going!",
                    'type': 'goal_suggestion',
                    'category': 'Goals',
                    'priority': 'low'
                })
            elif 49 <= progress_pct < 51:
                suggestions.append({
                    'text': f"🎉 Halfway there! You've reached 50% of your '{goal['goal_name']}' goal!",
                    'type': 'goal_suggestion',
                    'category': 'Goals',
                    'priority': 'low'
                })
            elif 74 <= progress_pct < 76:
                suggestions.append({
                    'text': f"🎉 Amazing! You're 75% done with your '{goal['goal_name']}' goal!",
                    'type': 'goal_suggestion',
                    'category': 'Goals',
                    'priority': 'low'
                })
            elif progress_pct >= 95:
                suggestions.append({
                    'text': f"🏁 Almost there! Just ₹{remaining:.0f} more to complete your '{goal['goal_name']}' goal!",
                    'type': 'goal_suggestion',
                    'category': 'Goals',
                    'priority': 'high'
                })
            
            # No contributions warning
            contrib_query = """
                SELECT COUNT(*) as count FROM goal_contributions 
                WHERE goal_id = %s AND contribution_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            """
            recent_contribs = DatabaseManager.execute_query(contrib_query, (goal['id'],), fetch=True)
            
            if recent_contribs and recent_contribs[0]['count'] == 0 and current_amount > 0:
                suggestions.append({
                    'text': f"💤 No contributions to '{goal['goal_name']}' in the last 30 days. Even small contributions add up!",
                    'type': 'goal_suggestion',
                    'category': 'Goals',
                    'priority': 'medium'
                })
        
        # Check if user has too many active goals
        if len(goals) > 5:
            suggestions.append({
                'text': f"📊 You have {len(goals)} active goals. Consider prioritizing 3-5 main goals to stay focused.",
                'type': 'goal_suggestion',
                'category': 'Goals',
                'priority': 'medium'
            })
        
    except Exception as e:
        print(f"Error generating goal suggestions: {e}")
    
    return suggestions