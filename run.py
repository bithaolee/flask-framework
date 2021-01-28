import yaml
from flask import Flask, g, request

from app import create_app


application = create_app()

if __name__ == '__main__':
    application.run(debug=True, host='localhost', port=8000)