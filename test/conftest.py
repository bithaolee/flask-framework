import os
import json

import pytest


@pytest.fixture
def app():
    from app import create_app
    return create_app()


@pytest.fixture
def client(app):
    app.config['TESTING'] = True
    with app.app_context():
        client = app.test_client()
        yield client


def login(client, username, password):
    return client.post(
        '/user/login',
        json={
            'username': username,
            'password': password,
        },
    )