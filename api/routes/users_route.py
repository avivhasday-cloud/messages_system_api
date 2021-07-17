from flask import Blueprint
from flask_restful import Api
from api.resources.users import Login, CreateUser
from api.utilities.errors import errors


users_bp = Blueprint('users_bp', __name__)
api = Api(users_bp, errors=errors)


api.add_resource(CreateUser, '/')
api.add_resource(Login, '/login')
