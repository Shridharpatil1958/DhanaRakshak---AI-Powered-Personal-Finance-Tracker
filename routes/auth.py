from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
import bcrypt
import jwt
from datetime import datetime, timedelta
from functools import wraps
from config import Config
from utils.db_utils import DatabaseManager

auth_bp = Blueprint('auth', __name__)

def token_required(f):
    """Decorator to protect routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = session.get('user_id')
        
        if not user_id:
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    
    return decorated

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'GET':
        return render_template('register.html')
    
    try:
        data = request.form
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')
        
        # Validation
        errors = []
        
        if not username or len(username) < 3:
            errors.append("Username must be at least 3 characters")
        
        if not email or '@' not in email:
            errors.append("Valid email is required")
        
        if not password or len(password) < 6:
            errors.append("Password must be at least 6 characters")
        
        if password != confirm_password:
            errors.append("Passwords do not match")
        
        if errors:
            return render_template('register.html', errors=errors)
        
        # Check if user exists
        check_query = "SELECT id FROM users WHERE username = %s OR email = %s"
        existing = DatabaseManager.execute_query(check_query, (username, email), fetch=True)
        
        if existing:
            return render_template('register.html', errors=["Username or email already exists"])
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Insert user
        insert_query = """
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
        """
        user_id = DatabaseManager.execute_query(insert_query, (username, email, password_hash))
        
        # Set session
        session['user_id'] = user_id
        session['username'] = username
        
        return redirect(url_for('upload.upload_page'))
    
    except Exception as e:
        return render_template('register.html', errors=[f"Registration failed: {str(e)}"])

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'GET':
        return render_template('login.html')
    
    try:
        data = request.form
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return render_template('login.html', error="Username and password are required")
        
        # Get user
        query = "SELECT id, username, password_hash FROM users WHERE username = %s OR email = %s"
        users = DatabaseManager.execute_query(query, (username, username), fetch=True)
        
        if not users:
            return render_template('login.html', error="Invalid credentials")
        
        user = users[0]
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return render_template('login.html', error="Invalid credentials")
        
        # Set session
        session['user_id'] = user['id']
        session['username'] = user['username']
        
        return redirect(url_for('upload.upload_page'))
    
    except Exception as e:
        return render_template('login.html', error=f"Login failed: {str(e)}")

@auth_bp.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/')
def index():
    """Home page - redirect to login"""
    if session.get('user_id'):
        return redirect(url_for('dashboard.dashboard_page'))
    return redirect(url_for('auth.login'))