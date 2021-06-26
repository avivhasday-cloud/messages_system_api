from flask import Flask, jsonify, request
from database import DataBase 
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from validations import user_validations, message_validations
import os
from werkzeug.security import generate_password_hash, check_password_hash


from dotenv import load_dotenv
from pathlib import Path  
import os

# set path to env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


app = Flask(__name__)
db = DataBase()
app.config["JWT_SECRET_KEY"] = os.getenv('SECRET_KEY')
jwt = JWTManager(app)
salt = "1Ha7"

"""
*****************************************************
Function: create_user
Request body arguments: username, email, password

validate request data
hash password
create user if the user doesnt exist in the system
returns user created or error message
*****************************************************
"""
@app.route('/users/', methods=['POST'])
def create_user():
    data = request.get_json()
    error_message = user_validations(data)
    if error_message:
        return jsonify({"Message": error_message}), 400

    username = data['username']
    email = data['email']
    hashed_password = generate_password_hash(data['password'], method='md5')
    if db.get_user(username):
        return jsonify({"Message": "Username already exists!"}), 400
 
    response = db.create_user(username, email, hashed_password)
    return jsonify(response), 200


"""
*****************************************************
Function: login
Request body arguments: username, password

validate request data
get user from database filter by username
returns error messge if the user doesnt exists
verify hashed password and password are equal
create a token with an identity of the user id
returns access token 
*****************************************************
"""
@app.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"Message" : "Username or password is missing!"}), 400

    user = db.get_user(username)
    print(user)
    if not user:
        return jsonify({"Message" : "Incorrect username!"}), 401

    if not check_password_hash(user['password'], password):
        return jsonify({"Message" : "Incorrect password!"}), 401

    # creating a token with user_id as identity 
    access_token = create_access_token(identity=user['id'])
    return jsonify(access_token=access_token), 200


"""
*****************************************************
Function: get_all_messages_for_user
Token format: Bearer + access_token

verify token
get user_id from token
get all the messages for the logged in user
returns all messages
*****************************************************
"""
@app.route('/messages/', methods=['GET'])
@jwt_required()
def get_all_messages_for_user():
    user_id = get_jwt_identity()
    response = db.get_all_messages_for_user(user_id)
    return jsonify(response)


"""
*****************************************************
Function: get_all_unread_messages_for_user
Token format: Bearer + access_token

verify token
get user_id from token
get all the unread messages for the logged in user
returns unread messages
*****************************************************
"""
@app.route('/messages/unread/', methods=['GET'])
@jwt_required()
def get_all_unread_messages_for_user():
    user_id = get_jwt_identity()
    response = db.get_all_unread_messages_for_user(user_id)
    return jsonify(response)


"""
*****************************************************
Function: write_message
Request body arguments: sender, receiver, 
                        subject, content

Token format: Bearer + access_token

verify token
get user_id from token
get request data
validate data - sends error if the data is incorrect
send message
*****************************************************
"""
@app.route('/messages/', methods=['POST'])
@jwt_required()
def write_message():
    user_id = get_jwt_identity()
    data = request.get_json()
    error_message = message_validations(data)
    if error_message:
        return jsonify({"Message": error_message}), 400
 
    response = db.write_message(data, user_id)
    return jsonify(response), 200

"""
*****************************************************
Function: write_message
Parameters: message id
Token format: Bearer + access_token

verify token
update the read_status of the selected message
returns the updated message
*****************************************************
"""
@app.route('/messages/<int:id>', methods=['PUT'])
@jwt_required()
def read_message(id):
    response = db.read_message(id)
    return jsonify(response)


"""
*****************************************************
Function: delete_message
Parameters: message id
Token format: Bearer + access_token

verify token
delete message
returns deleted successfuly or error message
*****************************************************
"""
@app.route('/messages/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_message(id):
    user_id = get_jwt_identity()
    response = db.delete_message(id, user_id)
    return jsonify(response)

if __name__ == '__main__':
    app.run()
