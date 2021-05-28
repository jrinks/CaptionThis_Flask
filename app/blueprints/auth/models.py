from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import os
import base64


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    #posts = db.relationship('Post', backref='author', lazy='dynamic')
    #do we need posts in the User model ?
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime())
    #should token be Index=True, that's how Brian did it but I don't know if we want/need it?
    last_voted = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

#everything past this point is stuff I grabbed from Brian's project and I have not changed anything

    def __repr__(self):
        return f'<User | {self.username}>'

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user
