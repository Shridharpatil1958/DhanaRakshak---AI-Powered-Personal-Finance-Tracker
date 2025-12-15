"""
DhanaRakshak Setup Script
This script helps set up the DhanaRakshak application
"""

import os
import sys
import subprocess

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(text)
    print("="*60 + "\n")

def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required")
        return False
    
    print("✓ Python version is compatible")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print_header("Installing Python Dependencies")
    
    try:
        print("Installing packages from requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\n✓ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies")
        return False

def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    
    directories = ['uploads', 'models', 'ml']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created directory: {directory}")
        else:
            print(f"✓ Directory already exists: {directory}")
    
    return True

def check_mysql():
    """Check MySQL installation"""
    print_header("Checking MySQL")
    
    print("Please ensure MySQL is installed and running.")
    print("\nTo verify MySQL installation:")
    print("  - Windows: Check Services for 'MySQL' service")
    print("  - Linux/Mac: Run 'mysql --version' in terminal")
    
    response = input("\nIs MySQL installed and running? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        print("✓ MySQL check passed")
        return True
    else:
        print("❌ Please install and start MySQL before continuing")
        return False

def configure_database():
    """Guide user through database configuration"""
    print_header("Database Configuration")
    
    print("Please update the following in config.py:")
    print("  - MYSQL_HOST (default: localhost)")
    print("  - MYSQL_USER (default: root)")
    print("  - MYSQL_PASSWORD (your MySQL password)")
    print("  - MYSQL_DATABASE (default: dhanarakshak)")
    print("  - MYSQL_PORT (default: 3306)")
    
    response = input("\nHave you configured the database settings? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        print("✓ Database configuration confirmed")
        return True
    else:
        print("⚠ Please configure database settings in config.py before running the app")
        return False

def train_models():
    """Train ML models"""
    print_header("Training ML Models")
    
    response = input("Do you want to train ML models now? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        try:
            print("\nTraining models... This may take a few minutes.")
            subprocess.check_call([sys.executable, "ml/train_models.py"])
            print("\n✓ ML models trained successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Error training models")
            return False
    else:
        print("⚠ You can train models later by running: python ml/train_models.py")
        return True

def print_next_steps():
    """Print next steps for the user"""
    print_header("Setup Complete!")
    
    print("Next steps:")
    print("\n1. Configure database settings in config.py (if not done)")
    print("2. Create MySQL database:")
    print("   mysql -u root -p")
    print("   CREATE DATABASE dhanarakshak;")
    print("   EXIT;")
    print("\n3. Train ML models (if not done):")
    print("   python ml/train_models.py")
    print("\n4. Run the application:")
    print("   python app.py")
    print("\n5. Access the application at:")
    print("   http://localhost:5000")
    print("\n6. Register a new account and start tracking your finances!")
    print("\n" + "="*60)

def main():
    """Main setup function"""
    print_header("DhanaRakshak Setup Wizard")
    print("Welcome! This wizard will help you set up DhanaRakshak.")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠ Warning: Some dependencies failed to install")
        response = input("Continue anyway? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Check MySQL
    if not check_mysql():
        print("\n⚠ Warning: MySQL check failed")
        response = input("Continue anyway? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            sys.exit(1)
    
    # Configure database
    configure_database()
    
    # Train models
    train_models()
    
    # Print next steps
    print_next_steps()

if __name__ == '__main__':
    main()