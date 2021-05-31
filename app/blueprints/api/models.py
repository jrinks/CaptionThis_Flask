from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from sqlalchemy import desc
import os
import base64


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(256), nullable=False)
    token = db.Column(db.String(32), index=True)
    token_expiration = db.Column(db.DateTime(), default=datetime.utcnow())
    last_voted = db.Column(db.DateTime, default=(datetime.utcnow() - timedelta(seconds=86401)))

    def __init__(self):
        self.username = ""
        self.email = ""
        self.password = ""
        self.token = ""
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email
        }

    def from_dict(self, data):
        for field in ['username', 'password', 'email']:
            if field in data:
                setattr(self, field, data[field])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit() 



#everything past this point is stuff I grabbed from Brian's project and I have not changed anything

    def __repr__(self):
        return f'<User | {self.username}>'

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token != "" and self.token_expiration > now + timedelta(seconds=60):
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


######Post Model##########

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    winner = db.relationship('Daily_Image', backref='winners', lazy='dynamic')
    post_body = db.Column(db.String(256))
    image_url = db.Column(db.String(256))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    votes = db.Column(db.Integer)


    def __init__(self):
    #not sure if I need to pass votes in here or not    
        self.post_body = ""
        self.image_url = ""
      
        
   
    
    def __repr__(self):
        return f'<Post | {self.id}>'

    def to_dict(self):
        username = User.query.filter_by(id=self.user_id).first().username
        return {
            'id': self.id,
            'post_body': self.post_body,
            'image_url': self.image_url,
            'date_created': self.date_created,
            'user_id': self.user_id,
            'votes': self.votes,
            'username': username
        }

    def from_dict(self, data):
        for field in ['post_body', 'image_url', 'date_created', 'user_id', 'votes']:
            if field in data:
                setattr(self, field, data[field])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit() 


#########Daily Image Model##############

class Daily_Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(256))
    winner = db.Column(db.Integer, db.ForeignKey('post.id'))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
 
    def __init__(self):
        self.image_url = ""

        
    def __repr__(self):
        return f'<Daily_Image | {self.image_url}>'

    def to_dict(self):
        winner_username = ""
        post_body = ""
        if Post.query.filter_by(id=self.winner).first():
            post_body = Post.query.filter_by(id=self.winner).first().post_body
        if Post.query.filter_by(id=self.winner).first():
            winner_username = Post.query.filter_by(id=self.winner).first().author.username
        return {
            'id': self.id,
            'image_url': self.image_url,
            'date_created': self.date_created,
            'winner': self.winner,
            'winner_username': winner_username,
            'post_body': post_body
        }

    def from_dict(self, data):
        for field in ['image_url']:
            if field in data:
                setattr(self, field, data[field])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def find_winner(self):
        winner = Post.query.order_by(desc('votes')).first()
        self.winner = winner.id
