from flask import Flask, session
from flask_cors import CORS
import os
from datetime import timedelta

# Import configuration
from config import Config

# Import routes
from routes.auth import auth_bp
from routes.upload import upload_bp
from routes.dashboard import dashboard_bp
from routes.api import api_bp, load_models

# Import utilities
from utils.db_utils import DatabaseManager

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Configure session
app.secret_key = Config.SECRET_KEY
app.permanent_session_lifetime = timedelta(days=7)

# Enable CORS
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(api_bp)

# Create necessary directories
os.makedirs('uploads', exist_ok=True)
os.makedirs('models', exist_ok=True)
os.makedirs('ml', exist_ok=True)

# Initialize database
@app.before_request
def initialize():
    """Initialize database and load models on first request"""
    if not hasattr(app, 'initialized'):
        print("Initializing DhanaRakshak...")
        
        # Initialize database
        try:
            DatabaseManager.initialize_database()
            print("✓ Database initialized")
        except Exception as e:
            print(f"✗ Database initialization failed: {e}")
        
        # Load ML models
        try:
            load_models()
            print("✓ ML models loaded")
        except Exception as e:
            print(f"✗ ML models loading failed: {e}")
            print("Note: Train models first using: python ml/train_models.py")
        
        app.initialized = True

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'app': 'DhanaRakshak'}, 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return {'error': 'Not found'}, 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return {'error': 'Internal server error'}, 500

if __name__ == '__main__':
    print("="*60)
    print("DhanaRakshak - AI Powered Personal Finance Tracker")
    print("="*60)
    print("\nStarting application...")
    print("\nIMPORTANT: Before running the app, please:")
    print("1. Set up MySQL database")
    print("2. Update database credentials in config.py")
    print("3. Train ML models: python ml/train_models.py")
    print("\nAccess the application at: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)