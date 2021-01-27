import yaml
from flask import Flask, g, request

from app.core.app import create_app


app = create_app('config.yml')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8000)