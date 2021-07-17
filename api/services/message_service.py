from api.utilities.errors import InternalServerError, MessageDoesntExistsError
from flask import jsonify, make_response
from api import db
from api.models.message_model import Message
from sqlalchemy import exc


def get_all_messages(user_id):
    """
        get all messages from database with the user id
    """
    try:
        messages = Message.query.filter(Message.user_id==user_id).all()
        return messages
    except exc.SQLAlchemyError:
        raise InternalServerError

def get_all_unread_messages(user_id):
    """
        get all unread messages from database with the user id
    """
    try:
        unread_messages = Message.query.filter_by(user_id=user_id, read_status=0).all()
        return unread_messages
    except exc.SQLAlchemyError:
        raise InternalServerError 

def write_message(data, user_id):
    """
        store the new message object in database
    """
    try:
        new_message = Message(
            user_id=user_id,
            sender=data['sender'],
            receiver=data['receiver'],
            subject=data['subject'],
            content=data['content']
        )
        save_changes(new_message)
        response_object = {
                'Status_code': 200,
                'Message': 'Message sent!'
        }
        return make_response(jsonify(response_object['Message']), response_object['Status_code'])
    except exc.SQLAlchemyError:
        raise InternalServerError


def read_message(message_id):
    """
        get message with the message id\n
        update the read status\n
        return the message
    """
    try:
        message_to_read = Message.query.filter_by(id=message_id).first()
        if not message_to_read:
            raise MessageDoesntExistsError

        message_to_read.read_status = 1
        db.session.commit()
        print(message_to_read)
        return message_to_read
    except exc.SQLAlchemyError:
        raise InternalServerError


def delete_message(message_id , user_id):
    """
        delete message filter by the message id and user id
    """
    try:
        message_to_delete = Message.query.filter_by(user_id=user_id, id=message_id).first()
        if not message_to_delete:
            raise MessageDoesntExistsError
        db.session.delete(message_to_delete)
        db.session.commit()
        response_object = {
                'Status_code': 200,
                'Message': 'Message deleted successfuly!'
        }
        return make_response(jsonify(response_object['Message']), response_object['Status_code'])
    except exc.SQLAlchemyError:
        raise InternalServerError

def save_changes(data):
    db.session.add(data)
    db.session.commit()