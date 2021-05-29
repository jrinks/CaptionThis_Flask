from app import db
from datetime import datetime
from app.blueprints.auth.models import User


######Post Model##########

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    winner = db.relationship('Daily_Image', backref='winners', lazy='dynamic')
    post_body = db.Column(db.String(256))
    image_url = db.Column(db.String(256))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    votes = db.Column(db.Integer)


    def __init__(self, post_body, image_url, date_created, user_id, votes = 0):
    #not sure if I need to pass votes in here or not    
        self.post_body = post_body
        self.user_id = user_id
        self.image_url = image_url
        self.date_created = date_created
        self.votes = votes
        
    def __repr__(self):
        return f'<Post | {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'post_body': self.post_body,
            'image_url': self.image_url,
            'date_created': self.date_created,
            'user_id': self.user_id,
            'votes': self.votes
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
 
    def __init__(self, image_url):
        self.image_url = image_url

        
    def __repr__(self):
        return f'<Daily_Image | {self.image_url}>'

    def to_dict(self):
        return {
            'id': self.id,
            'image_url': self.image_url,
            'date_created': self.date_created,
            'winner': self.winner
        }

    def from_dict(self, data):
        for field in ['image_url']:
            if field in data:
                setattr(self, field, data[field])
