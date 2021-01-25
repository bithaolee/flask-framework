import yaml
from flask import Flask, g

from app.core.error import handle_error
from app.handler import blueprints

def create_app():
    app = Flask(__name__)

    with open('config.yml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    app.config.from_mapping(config)

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    @app.teardown_appcontext
    def teardown_db():
        db = g.pop('_database', None)
        if db is not None:
            db.close()

    app.register_error_handler(Exception, handle_error)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='localhost', port=8000)