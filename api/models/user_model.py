from api import db, flask_bcrypt

class User(db.Model):
    """ 
        User Model for storing user related details 
    """
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        raise AttributeError('password not readable')

    @password.setter
    def password(self, password):
        self.hashed_password = flask_bcrypt.generate_password_hash(password).decode('utf-8')
        
    def verify_password(self, password):
        return flask_bcrypt.check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)