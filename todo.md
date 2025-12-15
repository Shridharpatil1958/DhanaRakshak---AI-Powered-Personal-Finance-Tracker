# DhanaRakshak - AI Powered Personal Finance Tracker

## Project Structure
```
dhanarakshak/
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── models/                         # Trained ML models
│   ├── expense_predictor.pkl
│   ├── savings_predictor.pkl
│   ├── bills_estimator.pkl
│   ├── anomaly_detector.pkl
│   └── budget_recommender.pkl
├── ml/                            # ML model training scripts
│   ├── train_models.py
│   ├── generate_dataset.py
│   └── model_utils.py
├── routes/                        # Flask route handlers
│   ├── __init__.py
│   ├── auth.py
│   ├── upload.py
│   ├── dashboard.py
│   └── api.py
├── utils/                         # Utility functions
│   ├── __init__.py
│   ├── db_utils.py
│   ├── file_processor.py
│   └── ai_suggestions.py
├── templates/                     # HTML templates
│   ├── base.html
│   ├── register.html
│   ├── login.html
│   ├── upload.html
│   └── dashboard.html
├── static/                        # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── dashboard.js
└── database/                      # Database setup
    └── schema.sql
```

## Development Tasks

### 1. Project Setup & Structure ✓
- Create Flask project structure
- Create requirements.txt with dependencies
- Create config.py for database and app settings

### 2. Database Design & Setup ✓
- Create schema.sql with all tables
- Implement database connection utilities
- Add indexes and foreign keys

### 3. User Authentication System ✓
- Build registration page with password hashing
- Build login page with JWT/session management
- Add logout functionality and route protection

### 4. Data Upload Module ✓
- Create upload page with 4 upload options
- Implement file processing with pandas
- Store transactions in MySQL

### 5. ML Model Development ✓
- Generate synthetic training dataset
- Train 5 ML models (expense, savings, bills, anomaly, budget)
- Save models using joblib

### 6. Flask API Layer ✓
- Create REST API endpoints for all models
- Load models on startup
- Return JSON predictions

### 7. Dashboard Page ✓
- Build dashboard with 5 predictions
- Add 4+ Chart.js visualizations
- Display AI suggestions

### 8. AI Suggestions Engine ✓
- Implement suggestion generator
- Analyze spending patterns
- Generate personalized tips

### 9. Frontend Integration ✓
- Connect Flask routes to templates
- Integrate Chart.js visualizations
- Add Bootstrap styling

### 10. Security & Production Readiness ✓
- Add input validation
- Implement error handling
- Secure routes with authentication
- Add CSRF protection