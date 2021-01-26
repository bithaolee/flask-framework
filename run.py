import yaml
from flask import Flask, g, request

from app.core.error import handle_error
from app.core.config import load_config, config


load_config('config.yml')


def create_app():
    app = Flask(__name__)

    app.config.debug = config('debug')

    from app.handler import blueprints
    from app.service.user import UserService

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

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='localhost', port=8000)