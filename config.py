"""
Application configuration.

Centralizes all settings that currently look like they're hardcoded in
app.py / init_db.py (MySQL credentials, secret key, upload limits). Reads
from environment variables with sane local-dev defaults, and is imported
by app.py as:

    from config import get_config
    app.config.from_object(get_config())
"""
import os


class BaseConfig:
    """Settings shared by every environment."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    # --- MySQL (mirrors database/schema.sql) ---
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_DB = os.environ.get("MYSQL_DB", "dhanarakshak")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- File uploads (CSV/Excel bank statements) ---
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
    ALLOWED_UPLOAD_EXTENSIONS = {"csv", "xlsx", "xls"}

    # --- ML model artifacts ---
    MODEL_DIR = os.environ.get("MODEL_DIR", "models")
    EXPENSE_MODEL_PATH = os.path.join(MODEL_DIR, "expense_predictor.pkl")
    SAVINGS_MODEL_PATH = os.path.join(MODEL_DIR, "savings_predictor.pkl")
    BILLS_MODEL_PATH = os.path.join(MODEL_DIR, "bills_estimator.pkl")
    ANOMALY_MODEL_PATH = os.path.join(MODEL_DIR, "anomaly_detector.pkl")
    BUDGET_MODEL_PATH = os.path.join(MODEL_DIR, "budget_recommender.pkl")

    # --- Sessions ---
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24  # 24 hours


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    DEBUG = False
    SESSION_COOKIE_SECURE = True

    def __init__(self):
        # Fail loudly on startup rather than silently using a dev secret
        # key in production.
        if os.environ.get("SECRET_KEY") is None:
            raise RuntimeError(
                "SECRET_KEY environment variable must be set in production."
            )


_CONFIGS = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config():
    """Return the config class selected by the FLASK_ENV env var."""
    env = os.environ.get("FLASK_ENV", "development")
    return _CONFIGS.get(env, DevelopmentConfig)
