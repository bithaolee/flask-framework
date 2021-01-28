import click
from flask.cli import AppGroup


test_cli = AppGroup('test')

@test_cli.command('hello')
@click.argument('name')
def hello(name):
    print('hello %s' % name)