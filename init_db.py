# init_db.py
import os
import mysql.connector
from config import Config

SCHEMA_FILE = os.path.join('database', 'schema.sql')

def load_schema(file_path):
    """Load SQL schema from file."""
    if not os.path.exists(file_path):
        print(f"✗ Error: Schema file not found at '{file_path}'")
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def init_db():
    print("="*60)
    print("DhanaRakshak Database Initialization")
    print("="*60)
    print("\nThis will create the database schema.")
    print("Make sure you have:")
    print("1. Created the database in MySQL")
    print("2. Updated database credentials in config.py\n")

    confirm = input("Continue? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Aborted.")
        return

    schema_sql = load_schema(SCHEMA_FILE)
    if not schema_sql:
        return

    try:
        print("\nConnecting to MySQL...")
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            port=Config.MYSQL_PORT,
            database=Config.MYSQL_DATABASE
        )
        cursor = conn.cursor()
        print("Connected successfully!")

        print("\nInitializing database...")
        for statement in schema_sql.split(';'):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)
        conn.commit()
        print("✔ Database initialized successfully!")

    except mysql.connector.Error as err:
        print(f"✗ MySQL Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    init_db()
