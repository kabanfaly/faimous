from celery import Celery
import os

_celery = None


def make_celery(flask_app=None):
    global _celery
    broker = os.environ.get("CELERY_BROKER_URL") or os.environ.get("REDIS_URL")
    backend = os.environ.get("CELERY_RESULT_BACKEND") or os.environ.get("REDIS_URL")
    if not broker:
        broker = "memory://"
    if not backend:
        backend = "memory://"
    celery = Celery("app", broker=broker, backend=backend)
    if flask_app:
        celery.conf.update(flask_app.config)
        celery.conf.update(
            task_serializer="json",
            accept_content=["json"],
            result_serializer="json",
            timezone="UTC",
            enable_utc=True,
        )
        TaskBase = celery.Task

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                with flask_app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)

        celery.Task = ContextTask
    _celery = celery
    return celery


def get_celery():
    return _celery
