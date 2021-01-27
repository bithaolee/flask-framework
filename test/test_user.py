import pytest

from .conftest import client, login


@pytest.mark.skip
def test_register(client):
    rv = client.post(
        '/user/register',
        json={
            'username': 'test@qq.com',
            'password': '123456789'
        }
    )
    resp = rv.get_json()
    assert resp['code'] == 0


def test_login(client):
    rv = login(client, 'test@qq.com', '123456789')
    resp = rv.get_json()
    assert resp['code'] == 0


