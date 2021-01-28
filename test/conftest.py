import os
import json

import pytest


@pytest.fixture
def client():
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        client = app.test_client()
        yield client


@pytest.fixture
def runner():
    from app.cli import app
    # app = create_app()
    # app.config['TESTING'] = True
    # app.config['FLASK_APP'] = '/mnt/e/wsl/flask-framework/cli.py'
    with app.app_context():
        runner = app.test_cli_runner()
        yield runner


def login(client, username, password):
    return client.post(
        '/user/login',
        json={
            'username': username,
            'password': password,
        },
    )