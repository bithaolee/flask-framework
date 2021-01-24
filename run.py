from flask import Flask, g

from .app.core.error import register_error_handler
from .app.handler import blueprints


def create_app():
    app = Flask(__name__)
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    register_error_handler(app)

app = create_app()

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8000)