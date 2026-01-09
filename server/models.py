from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields

from config import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    _password_hash = db.Column(db.String)

    # Protect the password_hash property (do not allow reading)
    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes may not be viewed.")

    # Hash the password and store it in _password_hash
    @password_hash.setter
    def password_hash(self, password):
        hashed = bcrypt.generate_password_hash(password.encode("utf-8"))
        self._password_hash = hashed.decode("utf-8")

    # Verify password against stored hash
    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash,
            password.encode("utf-8")
        )

    def __repr__(self):
        return f'User {self.username}, ID: {self.id}'

class UserSchema(Schema):
    id = fields.Int()
    username = fields.String()