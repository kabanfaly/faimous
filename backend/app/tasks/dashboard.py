from app.celery_app import get_celery

celery_app = get_celery()


@celery_app.task(name="dashboard.refresh_cache")
def refresh_dashboard_cache(organisation_id=None):
    """Optional task: refresh dashboard summary cache in Redis for an organisation or all."""
    return {"status": "ok", "organisation_id": organisation_id}
