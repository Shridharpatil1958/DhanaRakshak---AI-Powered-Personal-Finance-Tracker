<img width="1883" height="909" alt="Screenshot 2025-12-15 204351" src="https://github.com/user-attachments/assets/7b7d0791-3dc2-4d0c-adde-5ee5f57c3940" /># DhanaRakshak - AI Powered Personal Finance Tracker

A complete, production-ready AI-powered personal finance tracking application built with Flask, MySQL, and Machine Learning.

## 🎯 Features

### Core Functionality
- **User Authentication**: Secure registration and login with password hashing
- **Data Upload**: Multiple upload options (CSV, Excel, Manual Entry)
- **AI Predictions**: 
  - Next month expense prediction
  - Monthly savings prediction
  - Upcoming bills estimation
  - Anomaly detection
  - Budget recommendations
- **Interactive Dashboard**: Real-time visualizations with Chart.js
- **AI-Powered Suggestions**: Personalized financial insights and recommendations

### Technical Features
- **Backend**: Python Flask with RESTful APIs
- **Database**: MySQL with proper schema design
- **ML Models**: 5 trained models using Scikit-Learn
- **Frontend**: Bootstrap 5 with responsive design
- **Security**: Password hashing, session management, input validation

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

## 🚀 Installation & Setup

### 1. Clone or Download the Project

```bash
cd dhanarakshak
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up MySQL Database

#### Option A: Using MySQL Command Line

```bash
mysql -u root -p
```

Then create the database:

```sql
CREATE DATABASE dhanarakshak;
EXIT;
```

#### Option B: Using MySQL Workbench

1. Open MySQL Workbench
2. Connect to your MySQL server
3. Create a new database named `dhanarakshak`

### 4. Configure Database Connection

Edit `config.py` and update the MySQL credentials:

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'your_mysql_username'
MYSQL_PASSWORD = 'your_mysql_password'
MYSQL_DATABASE = 'dhanarakshak'
MYSQL_PORT = 3306
```

### 5. Train ML Models

Generate synthetic data and train all ML models:

```bash
cd ml
python train_models.py
cd ..
```

This will:
- Generate a synthetic financial dataset
- Train 5 ML models (Expense Predictor, Savings Predictor, Bills Estimator, Anomaly Detector, Budget Recommender)
- Save trained models in the `models/` directory

Expected output:
```
==================================================
DhanaRakshak ML Model Training
==================================================

Generating synthetic dataset...
Dataset generated: synthetic_finance_data.csv
Total records: 20000

Training Models...
==================================================

✓ Expense Predictor trained (Score: 0.XXX)
✓ Savings Predictor trained (Score: 0.XXX)
✓ Bills Estimator trained (Score: 0.XXX)
✓ Anomaly Detector trained
✓ Budget Recommender trained (Score: 0.XXX)

==================================================
✓ All models trained successfully!
==================================================
```

### 6. Run the Application

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## 📊 Using the Application

### 1. Register a New Account
- Navigate to `http://localhost:5000`
- Click "Register here"
- Fill in username, email, and password
- Submit the form

### 2. Upload Financial Data

#### Option A: Upload CSV/Excel File
- Click "Upload Data" in the navigation
- Select file type (CSV or Excel)
- Choose your file (must contain: date, amount, category columns)
- Click "Upload File"

#### Option B: Manual Entry
- Click "Upload Data"
- Fill in the manual entry form
- Select date, type, amount, category, etc.
- Click "Add Transaction"

#### Option C: Use Provided Dataset
- Use the provided `dhanarakshak_large_dataset.csv` file
- Upload it through the web interface

### 3. View Dashboard
- After uploading data, you'll be redirected to the dashboard
- View statistics, predictions, visualizations, and AI suggestions

### 4. Get AI Predictions
- Click prediction buttons to get:
  - Next month expense forecast
  - Monthly savings prediction
  - Upcoming bills estimation
  - Anomaly detection results

## 📁 Project Structure

```
dhanarakshak/
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── database/
│   └── schema.sql                  # MySQL database schema
│
├── models/                         # Trained ML models (generated)
│   ├── expense_predictor.pkl
│   ├── savings_predictor.pkl
│   ├── bills_estimator.pkl
│   ├── anomaly_detector.pkl
│   ├── budget_recommender.pkl
│   └── *_encoder.pkl
│
├── ml/                            # ML training scripts
│   ├── train_models.py            # Train all models
│   ├── generate_dataset.py        # Generate synthetic data
│   └── model_utils.py             # ML utility functions
│
├── routes/                        # Flask route handlers
│   ├── __init__.py
│   ├── auth.py                    # Authentication routes
│   ├── upload.py                  # Data upload routes
│   ├── dashboard.py               # Dashboard routes
│   └── api.py                     # ML API endpoints
│
├── utils/                         # Utility functions
│   ├── __init__.py
│   ├── db_utils.py                # Database utilities
│   ├── file_processor.py          # File processing
│   └── ai_suggestions.py          # AI suggestion engine
│
├── templates/                     # HTML templates
│   ├── base.html                  # Base template
│   ├── register.html              # Registration page
│   ├── login.html                 # Login page
│   ├── upload.html                # Upload page
│   └── dashboard.html             # Dashboard page
│
└── static/                        # Static files
    ├── css/
    │   └── style.css              # Custom styles
    └── js/
        └── dashboard.js           # Dashboard JavaScript
```

## 🔒 Security Features

- **Password Hashing**: Using bcrypt for secure password storage
- **Session Management**: Flask sessions with secure cookies
- **Input Validation**: Server-side validation for all inputs
- **SQL Injection Protection**: Parameterized queries
- **CSRF Protection**: Built-in Flask security
- **Error Handling**: Comprehensive error handling

## 🤖 Machine Learning Models

### 1. Expense Prediction Model
- **Algorithm**: Random Forest Regressor
- **Purpose**: Predict next month's total expenses
- **Features**: Month, day of week, category, user patterns

### 2. Savings Prediction Model
- **Algorithm**: Linear Regression
- **Purpose**: Predict monthly savings
- **Features**: Income, expenses, historical trends

### 3. Bills Estimation Model
- **Algorithm**: Random Forest Regressor
- **Purpose**: Estimate upcoming bills
- **Features**: Bill category, historical amounts, payment patterns

### 4. Anomaly Detection Model
- **Algorithm**: Isolation Forest
- **Purpose**: Detect unusual spending behavior
- **Features**: Transaction amount, category statistics

### 5. Budget Recommendation Model
- **Algorithm**: Random Forest Regressor
- **Purpose**: Suggest optimal category-wise budgets
- **Features**: Total expenses, category patterns, user behavior

## 📊 API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### Data Upload
- `GET /upload` - Upload page
- `POST /upload` - Process uploaded data

### Dashboard
- `GET /dashboard` - Dashboard page
- `GET /api/dashboard/data` - Get visualization data

### ML Predictions
- `POST /api/predict/expenses` - Predict next month expenses
- `POST /api/predict/savings` - Predict monthly savings
- `POST /api/predict/bills` - Estimate upcoming bills
- `POST /api/detect/anomalies` - Detect anomalous transactions
- `POST /api/recommend/budget` - Get budget recommendations

## 🎨 Dashboard Visualizations

1. **Monthly Expenses Trend**: Line chart showing expense trends over time
2. **Category-wise Spending**: Pie chart of spending by category
3. **Income vs Expense**: Bar chart comparing income and expenses
4. **Spending Distribution**: Histogram of transaction amounts

## 🔧 Troubleshooting

### Database Connection Error
```
Error: Can't connect to MySQL server
```
**Solution**: Check MySQL credentials in `config.py` and ensure MySQL service is running

### Models Not Found
```
Model not found: models/expense_predictor.pkl
```
**Solution**: Run `python ml/train_models.py` to train models

### Import Errors
```
ModuleNotFoundError: No module named 'flask'
```
**Solution**: Install dependencies with `pip install -r requirements.txt`

### Port Already in Use
```
Address already in use
```
**Solution**: Change port in `app.py` or kill the process using port 5000

## 📝 Dataset Format

Your CSV/Excel file should have these columns:

**Required:**
- `date` - Transaction date (YYYY-MM-DD)
- `amount` - Transaction amount (numeric)
- `category` - Expense category (Food, Rent, Bills, etc.)

**Optional:**
- `transaction_type` - income or expense (default: expense)
- `merchant` - Merchant name (default: Unknown)
- `payment_mode` - UPI, Credit Card, etc. (default: Other)
- `description` - Additional notes

**Example:**
```csv
date,amount,category,transaction_type,merchant,payment_mode
2024-01-15,500,Food,expense,Swiggy,UPI
2024-01-20,50000,Salary,income,Company,Bank Transfer
2024-01-25,2000,Shopping,expense,Amazon,Credit Card
```

## 🌟 Future Enhancements

- Goal setting and tracking
- Investment portfolio tracking
- Bill payment reminders
- Export reports to PDF
- Mobile app integration
- Multi-currency support
- Automated bank statement parsing
- Social comparison features

## 📸 Screenshots

### Login Page
Clean and secure authentication interface

### Dashboard
Interactive visualizations with real-time data

### AI Predictions
Machine learning powered financial forecasts

### AI Suggestions
Personalized insights and recommendations

## 🎓 Technical Details

### Database Schema
- **users**: User accounts with hashed passwords
- **transactions**: All financial transactions
- **predictions**: ML model predictions
- **ai_suggestions**: Generated AI insights
- **user_budgets**: Budget allocations

### ML Pipeline
1. Data preprocessing and cleaning
2. Feature engineering
3. Model training with cross-validation
4. Model evaluation and selection
5. Prediction serving via REST APIs

### Security Measures
- Bcrypt password hashing with salt
- Session-based authentication
- Input sanitization
- Parameterized SQL queries
- HTTPS ready (configure with SSL certificates)

## 📄 License

This project is created for educational and demonstration purposes.

## 👥 Contributors

DhanaRakshak Development Team

## 📞 Support

For technical support or questions:
1. Check the troubleshooting section
2. Review the documentation
3. Check database and ML model setup

---

**Note**: This is a production-ready application. Make sure to:
1. Update database credentials before deployment
2. Set strong SECRET_KEY in production
3. Enable HTTPS for production deployment
4. Regular database backups
5. Monitor ML model performance


**Happy Financial Tracking! 💰📊**
<img width="1883" height="909" alt="Screenshot 2025-12-15 204351" src="https://github.com/user-attachments/assets/6386004b-4728-4aad-9f2f-0ab0d716617f" />

