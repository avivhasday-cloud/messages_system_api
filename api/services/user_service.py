# from api.utilities.errors import LoginDetailsIsMissingError
from api.utilities.errors import IncorrectPasswordError, IncorrectUsernameError, UsernameAlreadyExistsError
from flask import jsonify, make_response
from api import db
from api.models.user_model import User
from flask_jwt_extended import create_access_token


def create_user(data):
    user = get_user(data['username'])
    if not user:
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        save_changes(new_user)
        response_object = {
            'Status_code': 201,
            'Message': 'Successfully registered.'
        }
        
        return make_response(jsonify(response_object['Message']), response_object['Status_code'])
    else:
        raise UsernameAlreadyExistsError
        

def login(data):
    username = data.get('username')
    password = data.get('password')
    user = get_user(username)
    if user is None:
        raise IncorrectUsernameError

    if user.verify_password(password) is None:
        raise IncorrectPasswordError
        
    else:
        print(user.id)
        token = create_access_token(identity=user.id)
        response_object = {
            'Status_code':200,
            'Message':{'Access Token': token}
        }
        return make_response(jsonify(response_object['Message']), response_object['Status_code'])


def get_user(username):
    return User.query.filter_by(username=username).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()