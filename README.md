A complete, production-ready AI-powered personal finance tracking application built with Flask, MySQL, and Machine Learning.

**Happy Financial Tracking! 💰📊**
<img width="1862" height="879" alt="Screenshot 2025-12-15 204245" src="https://github.com/user-attachments/assets/b3c7ba92-6bb3-4430-9572-731a2f8146df" />
<img width="1870" height="917" alt="Screenshot 2025-12-15 204219" src="https://github.com/user-attachments/assets/cdb2f6b6-68ce-4153-af85-9218dd81e2ae" />
<img width="1864" height="922" alt="Screenshot 2025-12-15 204311" src="https://github.com/user-attachments/assets/5b2e78f7-5d31-4a89-9134-82b8ca0c91fa" />
<img width="1886" height="913" alt="Screenshot 2025-12-15 204334" src="https://github.com/user-attachments/assets/c86ea462-b23c-44ed-91e5-78449292673c" />
<img width="1883" height="909" alt="Screenshot 2025-12-15 204351" src="https://github.com/user-attachments/assets/cccfb3f3-b3fe-43a6-90bc-df046db3671d" />


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


