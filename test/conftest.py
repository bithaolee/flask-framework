import os
import json

import pytest

from app.core.app import create_app


@pytest.fixture
def client():
    app = create_app('config.yml')
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