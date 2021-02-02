import uuid
import json

from flask import Blueprint, request, jsonify
from wtforms import Form, StringField, validators

from ..core.error import Code, AppException
# from ..service.user import UserService


user_blueprint = Blueprint(
    'user',
    __name__,
    url_prefix='/user'
)


class LoginForm(Form):
    username = StringField('username', validators=[validators.Length(min=8, max=12)])
    password = StringField('password', validators=[validators.Length(min=8, max=12)])

class RegisterForm(Form):
    username = StringField('username', validators=[validators.Length(min=8, max=12)])
    password = StringField('password', validators=[validators.Length(min=8, max=12)])

@user_blueprint.route('/register', methods=['POST'])
def register():
    form = RegisterForm(**request.json)
    if not form.validate():
        raise AppException(code=Code.INVALID_INPUT, msg='Invalid input', data=form.errors)
    
    # user_service = UserService()
    # user = user_service.get_user_by_username(form.data['username'])
    # if user:
    #     raise AppException(code=Code.INVALID_INPUT, msg='User has been existed', data=[])

    # user_service.add_user(form.data['username'], form.data['password'])

    return jsonify(dict(code=Code.OK, msg='ok'))

@user_blueprint.route('/login', methods=['POST'])
def login():
    form = LoginForm(**request.json)
    if not form.validate():
        raise AppException(code=Code.INVALID_INPUT, msg='Invalid input', data=form.errors)
    
    # user_service = UserService()

    # user = user_service.get_user_by_username(form.data['username'])
    # if not user:
    #     raise AppException(code=Code.INVALID_INPUT, msg='User not found', data=[])

    token = uuid.uuid4()
    # user_service.save_token(token, user)

    return jsonify(dict(code=Code.OK, msg='ok', data=dict(token=token)))