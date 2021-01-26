import yaml
from flask import Flask, g, request

from app.core.error import handle_error
from app.handler import blueprints


def create_app():
    app = Flask(__name__)

    ctx = app.app_context()
    ctx.push()

    with open('config.yml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    app.config.from_mapping(config)

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    from app.service.user import UserService
    from app.core.db import close_db

    @app.before_request
    def before_request():
        token = request.headers.get('token', None)
        if token is not None:
            user = UserService().get_user_by_token(token)
            if user is not None:
                g.user = user

    app.teardown_appcontext(close_db)
    app.register_error_handler(Exception, handle_error)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='localhost', port=8000)