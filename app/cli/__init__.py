import click

from .. import create_app
from .test import test_cli


app = create_app()
app.cli.add_command(test_cli)
