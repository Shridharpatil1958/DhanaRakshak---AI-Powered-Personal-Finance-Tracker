# DhanaRakshak - Quick Start Guide

Get DhanaRakshak up and running in 5 minutes!

## ⚡ Quick Setup

### Step 1: Install Dependencies (2 minutes)

```bash
# Install Python packages
pip install -r requirements.txt
```

### Step 2: Setup MySQL Database (1 minute)

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE dhanarakshak;
EXIT;
```

### Step 3: Configure Database (30 seconds)

Edit `config.py`:

```python
MYSQL_USER = 'root'          # Your MySQL username
MYSQL_PASSWORD = 'password'  # Your MySQL password
```

### Step 4: Train ML Models (1 minute)

```bash
cd ml
python train_models.py
cd ..
```

### Step 5: Run Application (30 seconds)

```bash
python app.py
```

Visit: `http://localhost:5000`

## 🎯 First Steps

1. **Register**: Create your account
2. **Upload Data**: Upload the provided CSV file or add transactions manually
3. **View Dashboard**: See your financial insights
4. **Get Predictions**: Click prediction buttons for AI insights

## 📝 Sample Data

Use the provided `dhanarakshak_large_dataset.csv` file to test the application with pre-populated data.

## 🆘 Common Issues

### Issue: "Can't connect to MySQL"
**Solution**: Check MySQL is running and credentials in `config.py` are correct

### Issue: "Models not found"
**Solution**: Run `python ml/train_models.py` to train models

### Issue: "Module not found"
**Solution**: Run `pip install -r requirements.txt`

## 📚 Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Explore the dashboard features
- Try different ML predictions

## 🎉 You're Ready!

Start tracking your finances with AI-powered insights!