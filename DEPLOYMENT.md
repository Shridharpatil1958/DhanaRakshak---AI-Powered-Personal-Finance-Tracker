# DhanaRakshak Deployment Guide

This guide provides instructions for deploying DhanaRakshak to production environments.

## 🚀 Production Deployment

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- Web server (Nginx/Apache)
- WSGI server (Gunicorn/uWSGI)
- SSL certificate (for HTTPS)

## 📦 Deployment Options

### Option 1: Traditional Server Deployment

#### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv mysql-server nginx -y

# Install Gunicorn
pip3 install gunicorn
```

#### 2. Application Setup

```bash
# Clone/upload application
cd /var/www/
sudo mkdir dhanarakshak
sudo chown $USER:$USER dhanarakshak
cd dhanarakshak

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn
```

#### 3. Configure MySQL

```bash
# Secure MySQL installation
sudo mysql_secure_installation

# Create database
sudo mysql -u root -p
```

```sql
CREATE DATABASE dhanarakshak;
CREATE USER 'dhanarakshak_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON dhanarakshak.* TO 'dhanarakshak_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 4. Update Configuration

Edit `config.py`:

```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-production-secret-key'
    
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'dhanarakshak_user'
    MYSQL_PASSWORD = 'strong_password'
    MYSQL_DATABASE = 'dhanarakshak'
    MYSQL_PORT = 3306
    
    # Production settings
    DEBUG = False
    TESTING = False
```

#### 5. Train ML Models

```bash
cd ml
python train_models.py
cd ..
```

#### 6. Create Gunicorn Service

Create `/etc/systemd/system/dhanarakshak.service`:

```ini
[Unit]
Description=DhanaRakshak Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/dhanarakshak
Environment="PATH=/var/www/dhanarakshak/venv/bin"
ExecStart=/var/www/dhanarakshak/venv/bin/gunicorn --workers 4 --bind unix:dhanarakshak.sock -m 007 app:app

[Install]
WantedBy=multi-user.target
```

Start the service:

```bash
sudo systemctl start dhanarakshak
sudo systemctl enable dhanarakshak
sudo systemctl status dhanarakshak
```

#### 7. Configure Nginx

Create `/etc/nginx/sites-available/dhanarakshak`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/dhanarakshak/dhanarakshak.sock;
    }

    location /static {
        alias /var/www/dhanarakshak/static;
    }

    client_max_body_size 16M;
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/dhanarakshak /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

#### 8. Setup SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### Option 2: Docker Deployment

#### 1. Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy application
COPY . .

# Train models
RUN cd ml && python train_models.py && cd ..

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

#### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - MYSQL_HOST=db
      - MYSQL_USER=dhanarakshak
      - MYSQL_PASSWORD=password
      - MYSQL_DATABASE=dhanarakshak
    depends_on:
      - db
    volumes:
      - ./uploads:/app/uploads
      - ./models:/app/models

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
      - MYSQL_DATABASE=dhanarakshak
      - MYSQL_USER=dhanarakshak
      - MYSQL_PASSWORD=password
    volumes:
      - mysql_data:/var/lib/mysql
      - ./database/schema.sql:/docker-entrypoint-initdb.d/schema.sql

volumes:
  mysql_data:
```

#### 3. Deploy with Docker

```bash
docker-compose up -d
```

### Option 3: Cloud Platform Deployment

#### AWS Elastic Beanstalk

1. Install EB CLI:
```bash
pip install awsebcli
```

2. Initialize EB:
```bash
eb init -p python-3.9 dhanarakshak
```

3. Create environment:
```bash
eb create dhanarakshak-env
```

4. Deploy:
```bash
eb deploy
```

#### Heroku

1. Create `Procfile`:
```
web: gunicorn app:app
```

2. Deploy:
```bash
heroku create dhanarakshak
heroku addons:create cleardb:ignite
git push heroku main
```

## 🔒 Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use strong database passwords
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall (UFW/iptables)
- [ ] Set up regular database backups
- [ ] Enable rate limiting
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Disable debug mode in production
- [ ] Set up monitoring and logging
- [ ] Regular security updates
- [ ] Implement backup strategy

## 📊 Monitoring

### Setup Logging

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('dhanarakshak.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('DhanaRakshak startup')
```

### Database Backups

```bash
# Create backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u dhanarakshak_user -p dhanarakshak > /backups/dhanarakshak_$DATE.sql
find /backups -name "dhanarakshak_*.sql" -mtime +7 -delete
```

## 🔄 Updates and Maintenance

### Update Application

```bash
cd /var/www/dhanarakshak
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart dhanarakshak
```

### Database Migrations

```bash
# Backup before migration
mysqldump -u dhanarakshak_user -p dhanarakshak > backup_before_migration.sql

# Apply migrations
mysql -u dhanarakshak_user -p dhanarakshak < migration.sql
```

## 📈 Performance Optimization

1. **Enable Caching**: Use Redis or Memcached
2. **Database Indexing**: Ensure proper indexes
3. **Static File CDN**: Use CDN for static assets
4. **Load Balancing**: Use multiple application servers
5. **Database Connection Pooling**: Configure connection pools
6. **Gzip Compression**: Enable in Nginx
7. **Monitor Performance**: Use APM tools

## 🆘 Troubleshooting

### Application Won't Start

```bash
# Check logs
sudo journalctl -u dhanarakshak -n 50

# Check Gunicorn
sudo systemctl status dhanarakshak

# Check Nginx
sudo nginx -t
sudo systemctl status nginx
```

### Database Connection Issues

```bash
# Test MySQL connection
mysql -u dhanarakshak_user -p dhanarakshak

# Check MySQL status
sudo systemctl status mysql
```

### Permission Issues

```bash
# Fix ownership
sudo chown -R www-data:www-data /var/www/dhanarakshak

# Fix permissions
sudo chmod -R 755 /var/www/dhanarakshak
```

## 📞 Support

For deployment issues:
1. Check application logs
2. Check system logs
3. Verify all services are running
4. Check firewall rules
5. Verify database connectivity

---

**Note**: Always test deployment in a staging environment before production deployment.