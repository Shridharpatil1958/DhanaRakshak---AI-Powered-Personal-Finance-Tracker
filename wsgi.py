"""
Production WSGI entry point.

Local dev keeps using `python app.py` (Flask's built-in server). In
production, point a WSGI server at this module instead, e.g.:

    gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app

This avoids running Flask's debug/dev server in production, which is
not designed to be safe or performant for real traffic.
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
