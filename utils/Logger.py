"""
Centralized logging setup.

Usage in app.py:
    from utils.logger import setup_logging
    setup_logging(app)

Then anywhere in the app:
    import logging
    logging.getLogger(__name__).info("...")
"""
import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging(app):
    log_dir = os.environ.get("LOG_DIR", "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_level = logging.DEBUG if app.debug else logging.INFO

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "dhanarakshak.log"),
        maxBytes=1_000_000,
        backupCount=3,
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(log_level)

    app.logger.handlers.clear()
    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(log_level)

    # Quiet down noisy third-party loggers unless we're debugging.
    if not app.debug:
        logging.getLogger("werkzeug").setLevel(logging.WARNING)

    app.logger.info("Logging configured (level=%s)", logging.getLevelName(log_level))
