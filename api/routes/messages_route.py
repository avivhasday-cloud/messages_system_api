from flask import Blueprint
from flask_restful import Api
from api.resources.messages import Messages, UnreadMessages, Message
from api.utilities.errors import errors



messages_bp = Blueprint('messages_bp', __name__)
api = Api(messages_bp, errors=errors)


api.add_resource(Messages, '/') # GET - Get All Messages For User
api.add_resource(UnreadMessages, '/unread') # GET - Get All Unread Messages For User
api.add_resource(Message, '/', '/<int:message_id>') # POST -  WRITE MESSAGE
                                                    # PUT - Read Message
                                                    # DELETE - Delete Message
 



