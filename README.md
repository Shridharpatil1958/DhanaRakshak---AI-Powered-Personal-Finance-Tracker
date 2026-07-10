<div align="center">

# 💰 DhanaRakshak AI-Powered Personal Finance Management System

### Track Expenses • Predict Savings • Achieve Financial Goals

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?style=for-the-badge&logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql)
![Scikit-Learn](https://img.shields.io/badge/Machine%20Learning-ScikitLearn-F7931E?style=for-the-badge&logo=scikitlearn)
![Chart.js](https://img.shields.io/badge/Chart.js-Visualization-FF6384?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

</div>

---

# 🌟 Project Overview

**DhanaRakshak AI** is a complete AI-powered personal finance management platform that helps users monitor expenses, predict future financial trends, set savings goals, and receive intelligent financial recommendations.

The application combines:

✅ Personal Finance Tracking

✅ Machine Learning Predictions

✅ Financial Goal Management

✅ Interactive Dashboards

✅ AI-Powered Financial Assistant

✅ Secure Authentication System

---

# 🎯 Business Problem

Managing personal finances can be challenging due to:

- Uncontrolled spending
- Lack of savings planning
- Difficulty tracking expenses
- Poor budgeting decisions
- No future financial forecasting

DhanaRakshak AI solves these problems by providing intelligent insights and predictive analytics.

---

# 📸 Application Screenshots

## 📝 User Registration

### Secure Account Creation

Features:

- Input Validation
- Password Hashing
- Secure User Registration

<img width="100%" src="https://github.com/user-attachments/assets/b3c7ba92-6bb3-4430-9572-731a2f8146df" />

---

## 🔐 User Login

### Secure Authentication System

Features:

- Session Management
- Encrypted Credentials
- Secure Login Access

<img width="100%" src="https://github.com/user-attachments/assets/cdb2f6b6-68ce-4153-af85-9218dd81e2ae" />

---

## 📤 Financial Data Upload

### Income & Expense Upload Interface

Users can:

- Upload CSV Files
- Upload Excel Files
- Add Transactions Manually

<img width="100%" src="https://github.com/user-attachments/assets/5b2e78f7-5d31-4a89-9134-82b8ca0c91fa" />

---

## 🎯 Goal Setup Module

### Financial Goal Planning

Users can define:

- Savings Targets
- Time Duration
- Priority Levels

<img width="100%" src="https://github.com/user-attachments/assets/63190242-5263-40fd-b4b9-1e7974eecef7" />

---

## 📊 Goal Dashboard

### Goal Progress Tracking

Features:

- Goal Completion %
- Savings Progress
- Estimated Achievement Date

<img width="100%" src="https://github.com/user-attachments/assets/c054d1e5-f3d2-4660-a3e4-e6b5795fee5f" />

---

## 🤖 AI Financial Assistant

### Personalized Financial Recommendations

Features:

- Spending Insights
- Budget Suggestions
- Savings Recommendations
- Predictive Financial Advice

<img width="100%" src="https://github.com/user-attachments/assets/d02086bf-7c5e-4484-8eb1-40d17cc317b7" />

---

## 📈 Income vs Expense Dashboard

### Interactive Financial Analytics

Features:

- Income Analysis
- Expense Tracking
- Cash Flow Monitoring
- Category-wise Spending

<img width="100%" src="https://github.com/user-attachments/assets/c86ea462-b23c-44ed-91e5-78449292673c" />

<br>

<img width="100%" src="https://github.com/user-attachments/assets/cccfb3f3-b3fe-43a6-90bc-df046db3671d" />

---

# 🚀 Key Features

## 🔐 Authentication System

- User Registration
- Secure Login
- Password Hashing using Bcrypt
- Session Management

---

## 📊 Financial Tracking

- Expense Tracking
- Income Monitoring
- Budget Management
- Transaction History

---

## 🎯 Goal Management

- Create Financial Goals
- Track Goal Progress
- Savings Monitoring
- Achievement Predictions

---

## 🤖 AI Features

### Smart Predictions

- Next Month Expense Prediction
- Monthly Savings Prediction
- Upcoming Bills Estimation
- Budget Recommendations
- Spending Anomaly Detection

---

# 📂 Project Structure

```bash
DhanaRakshak-AI/
│
├── app.py
├── config.py
├── requirements.txt
│
├── database/
│   └── schema.sql
│
├── ml/
│   ├── train_models.py
│   ├── expense_predictor.py
│   ├── savings_predictor.py
│   ├── anomaly_detector.py
│   └── budget_recommender.py
│
├── models/
│   ├── expense_predictor.pkl
│   ├── savings_predictor.pkl
│   ├── bills_estimator.pkl
│   ├── anomaly_detector.pkl
│   └── budget_recommender.pkl
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── upload.html
│   ├── goals.html
│   └── assistant.html
│
├── uploads/
│
└── README.md
```

---

# 🔄 Application Workflow

```text
User Registration
        ↓
User Login
        ↓
Upload Financial Data
        ↓
Data Processing
        ↓
Machine Learning Analysis
        ↓
Predictions & Recommendations
        ↓
Dashboard Visualization
        ↓
Goal Tracking & Monitoring
```

---

# 🤖 Machine Learning Models

## Expense Prediction

### Algorithm

```python
Random Forest Regressor
```

Purpose:

- Predict future monthly expenses

---

## Savings Prediction

### Algorithm

```python
Linear Regression
```

Purpose:

- Forecast future savings

---

## Bills Estimation

### Algorithm

```python
Random Forest Regressor
```

Purpose:

- Estimate upcoming bills

---

## Anomaly Detection

### Algorithm

```python
Isolation Forest
```

Purpose:

- Detect unusual spending patterns

---

## Budget Recommendation

### Algorithm

```python
Random Forest Regressor
```

Purpose:

- Recommend category-wise budget allocation

---

# 📊 Dashboard Analytics

### Financial KPIs

- Total Income
- Total Expenses
- Net Savings
- Savings Rate

### AI Insights

- Future Expense Forecast
- Budget Recommendations
- Goal Achievement Probability
- Spending Risk Analysis

---

# 📋 Dataset Format

Required Columns:

```csv
date,amount,category
```

Optional Columns:

```csv
transaction_type
merchant
payment_mode
description
```

Example:

```csv
date,amount,category,transaction_type
2024-01-15,500,Food,expense
2024-01-20,50000,Salary,income
2024-01-25,2000,Shopping,expense
```

---

# 🛠️ Technologies Used

| Category | Technologies |
|-----------|-------------|
| Backend | Flask |
| Frontend | HTML, CSS, Bootstrap 5 |
| Database | MySQL |
| Machine Learning | Scikit-Learn |
| Data Analysis | Pandas, NumPy |
| Visualization | Chart.js |
| Authentication | Bcrypt |

---

# 🔒 Security Features

### Authentication Security

- Password Hashing
- Session Management
- Input Validation

### Database Security

- Parameterized Queries
- SQL Injection Protection

### Application Security

- Error Handling
- Secure Cookie Sessions
- User Access Control

---

# 📡 REST API Endpoints

## Authentication

```http
POST /register
POST /login
GET /logout
```

## Dashboard

```http
GET /dashboard
GET /api/dashboard/data
```

## Predictions

```http
POST /api/predict/expenses
POST /api/predict/savings
POST /api/predict/bills
POST /api/detect/anomalies
POST /api/recommend/budget
```

---

# 📈 Business Impact

DhanaRakshak AI helps users:

✅ Track Personal Finances

✅ Improve Savings Habits

✅ Detect Overspending

✅ Plan Financial Goals

✅ Forecast Future Expenses

✅ Make Data-Driven Financial Decisions

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/DhanaRakshak-AI.git
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure MySQL

```sql
CREATE DATABASE dhanarakshak;
```

## Train Models

```bash
python ml/train_models.py
```

## Run Application

```bash
python app.py
```

Open:

```text
http://localhost:5000
```

---

# 🔮 Future Enhancements

### Finance Features

- Investment Portfolio Tracking
- Loan Management
- Credit Score Monitoring
- Bill Payment Reminders

### AI Enhancements

- LLM-Based Financial Advisor
- Personalized Wealth Planning
- Spending Habit Analysis

### Deployment

- Docker Support
- AWS Deployment
- Mobile Application

---

# 🏆 Skills Demonstrated

### Data Science

- Machine Learning
- Predictive Analytics
- Anomaly Detection

### Software Development

- Flask Development
- REST APIs
- Database Design

### Analytics

- Data Visualization
- Financial Analytics
- KPI Monitoring

### AI

- Recommendation Systems
- Forecasting Models
- Intelligent Insights

---

# 👨‍💻 Author

## Shridhar Patil

🎓 Computer Science Engineer

📊 Data Analyst | Data Science Enthusiast

📧 shridharpatil0513@gmail.com

🐙 GitHub: https://github.com/Shridharpatil1958

---

# ⭐ Support

If you found this project useful:

⭐ Star the Repository

🍴 Fork the Project

📢 Share with Others

---

<div align="center">

### 💰 Empowering Smarter Financial Decisions Through AI

Made with ❤️ by Shridhar Patil

</div>
