from .conftest import runner
from app.cli import test


def test_test(runner):
    print(test)
    result = runner.invoke(test, ['lihao'])
    print(result)
    assert result == 'name: lihao'