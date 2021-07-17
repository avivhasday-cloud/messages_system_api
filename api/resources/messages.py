from flask_restful import Resource, reqparse, marshal_with, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.services import message_service

message_serializer = {
    'id':fields.Integer,
    'user_id':fields.Integer,
    'sender':fields.String,
    'receiver':fields.String,
    'subject':fields.String,
    'content':fields.String,
    'creation_date':fields.DateTime,
    'read_status':fields.Integer
}



write_messsage_parser = reqparse.RequestParser()
write_messsage_parser.add_argument('sender', help='Sender name is required!', required=True)
write_messsage_parser.add_argument('receiver', help='Receiver name is required!', required=True)
write_messsage_parser.add_argument('subject', help='Subject is required!', required=True)
write_messsage_parser.add_argument('content', help='Content is required!', required=True)


class Messages(Resource):
    """ 
        Authentication required\n
        Get all messages for user
    """
    method_decorators = [jwt_required()]
    @marshal_with(message_serializer, envelope='Messages')
    def get(self):
        user_id = get_jwt_identity()
        res = message_service.get_all_messages(user_id)
        return res

class UnreadMessages(Resource):
    """ 
        Authentication required\n
        Get all unread messages for user
    """
    method_decorators = [jwt_required()]
    @marshal_with(message_serializer, envelope='Unread Messages')
    def get(self):
        user_id = get_jwt_identity()
        res = message_service.get_all_unread_messages(user_id)
        return res


class Message(Resource):
    method_decorators = [jwt_required()] # check if the user logged in
    
    """
        Write message
        Arguments: sender, receiver, subject, content
        Return message sent or error
    """
    def post(self):
        user_id = get_jwt_identity()
        args = write_messsage_parser.parse_args()
        res = message_service.write_message(args, user_id)
        return res

    """
        Delete message
        url params: message id
        Return message deleted successfuly or error
    """
    def delete(self, message_id):
        user_id = get_jwt_identity()
        res = message_service.delete_message(message_id, user_id)
        return res

    """
        Read message
        url params: message id
        Return message
    """
    @marshal_with(message_serializer, envelope='Message')
    def put(self, message_id):
        res = message_service.read_message(message_id)
        return res


