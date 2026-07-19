"""
Shared input validation helpers.

Import from routes as:
    from utils.validators import validate_registration, allowed_file
"""
import re
import os

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# Mirrors config.ALLOWED_UPLOAD_EXTENSIONS; kept as a plain constant here so
# this module has no Flask/app-context dependency and stays easily testable.
ALLOWED_UPLOAD_EXTENSIONS = {"csv", "xlsx", "xls"}

REQUIRED_TRANSACTION_COLUMNS = {"date", "amount", "category"}


def validate_registration(username: str, email: str, password: str) -> list[str]:
    """Return a list of human-readable error messages (empty list = valid)."""
    errors = []

    if not username or len(username.strip()) < 3:
        errors.append("Username must be at least 3 characters long.")

    if not email or not EMAIL_RE.match(email):
        errors.append("Please enter a valid email address.")

    if not password or len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    elif not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter.")
    elif not re.search(r"[0-9]", password):
        errors.append("Password must contain at least one digit.")

    return errors


def validate_login(email: str, password: str) -> list[str]:
    errors = []
    if not email or not EMAIL_RE.match(email):
        errors.append("Please enter a valid email address.")
    if not password:
        errors.append("Password is required.")
    return errors


def allowed_file(filename: str) -> bool:
    """Check file extension only. Caller should still validate content
    (e.g. via pandas.read_csv failing gracefully) before trusting the file."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_UPLOAD_EXTENSIONS
    )


def validate_transaction_columns(columns) -> list[str]:
    """Check an uploaded CSV/Excel file has the columns app.py expects
    (see README 'Dataset Format': date, amount, category required)."""
    present = {c.strip().lower() for c in columns}
    missing = REQUIRED_TRANSACTION_COLUMNS - present
    if missing:
        return [f"Missing required column(s): {', '.join(sorted(missing))}"]
    return []


def safe_filename(filename: str) -> str:
    """Strip directory components so an uploaded filename can't be used for
    path traversal (e.g. '../../etc/passwd'). Prefer werkzeug.utils.secure_filename
    if it's already a dependency in app.py; this is a minimal fallback."""
    filename = os.path.basename(filename)
    filename = re.sub(r"[^A-Za-z0-9_.\-]", "_", filename)
    return filename
