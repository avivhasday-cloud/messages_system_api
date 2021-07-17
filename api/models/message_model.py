from sqlalchemy.dialects import mysql
from api import db
import datetime

class Message(db.Model):
    """ Message Model for storing messages related details """
    __tablename__ = "Messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    sender = db.Column(db.String(45), nullable=False)
    receiver = db.Column(db.String(45), nullable=False)
    subject = db.Column(db.String(45), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    read_status = db.Column(mysql.TINYINT(1), default=0)