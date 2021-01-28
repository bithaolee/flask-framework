from ..core.celery import create_celery
from .. import create_app


app = create_app()

celery = create_celery(app)

from . import test