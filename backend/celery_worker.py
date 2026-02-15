"""
Celery worker entry point. Run from backend/: celery -A celery_worker worker -l info
"""
from app import create_app
from app.celery_app import make_celery

app = create_app()
celery = make_celery(app)

# Import tasks so they are registered (after make_celery so get_celery() works)
import app.tasks.dashboard  # noqa: F401
