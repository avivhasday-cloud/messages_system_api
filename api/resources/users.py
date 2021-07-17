from flask_restful import Resource, reqparse
from api.services import user_service


# Adding arguments to login resource
user_login_parser = reqparse.RequestParser()
user_login_parser.add_argument('username', help='Username is required!', required=True)
user_login_parser.add_argument('password', help='Password is required', required=True)

# Adding arguments to create user resource
create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('username', help='Username is required!', required=True)
create_user_parser.add_argument('email', help='Email is required', required=True)
create_user_parser.add_argument('password', help='Password is required', required=True)


class Login(Resource):
    """
        Login user\n
        Arguments: username, password\n
        return access token or error
    """
    def post(self):
        args = user_login_parser.parse_args()
        res = user_service.login(args)
        return res

class CreateUser(Resource):
    """
        Create user\n
        Arguments: username, email, password\n
        return access token or error
    """
    def post(self):
        args = create_user_parser.parse_args()
        res = user_service.create_user(args)
        return res


