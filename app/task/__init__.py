from ..core.celery import create_celery
from ..core.app import create_app


app = create_app('config.yml')

celery = create_celery(app)

from . import test