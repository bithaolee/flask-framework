from celery import Celery
from .config import config


def create_celery(app):
    celery_cfg = config('celery')
    celery = Celery(
        app.import_name,
        backend=celery_cfg['backend'],
        broker=celery_cfg['broker'],
    )
    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone=config('timezone'),
        enable_utc=True,
        result_expires=3600,
    )


    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery