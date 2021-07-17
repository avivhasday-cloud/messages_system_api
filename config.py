from dotenv import load_dotenv
from pathlib import Path  # python3 only
import os



class Config:
    """
        Global configuration settings for the app
    """

    SQLALCHEMY_DATABASE_URI = os.getenv('MYSQL_CONNECTION')
    SQLALCHEMY_TRACK_MODIFICATIONS =os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    JWT_SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = False
