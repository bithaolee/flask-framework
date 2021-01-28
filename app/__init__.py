import yaml
from flask import Flask, g, request

from .core.error import handle_error
from .core.config import config


def create_app():

    app = Flask(__name__)

    cfg = config()

    app.config.update(dict(
        DEBUG=cfg['debug'],
        TESTING=cfg['debug'],
        SECRET_KEY=cfg['secret_key'],
    ))

    from .handler import blueprints
    from .service.user import UserService

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    app.register_error_handler(Exception, handle_error)

    @app.teardown_appcontext
    def close_db(e):
        db = g.pop('_database', None)
        if db is not None:
            db.close()

    @app.before_request
    def before_request():
        token = request.headers.get('Authorization', None)
        if token is not None:
            user = UserService().get_user_by_token(token)
            if user is not None:
                g.user = user

    return app
