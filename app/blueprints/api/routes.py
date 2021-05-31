from datetime import date, datetime, timedelta
from sqlite3 import Timestamp
from flask import request, jsonify
from flask_login import current_user
from app.blueprints.api.models import Post, User, UserMixin, Daily_Image
from app import db
from . import bp as api
from werkzeug.security import check_password_hash, generate_password_hash
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from sqlalchemy import desc

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


'''All api endpoint routes go here: 

1 create user (POST to user table)
2 login user (GET to user table)
3 Basic Auth
4 Token Auth
5 create a post (POST to post table)
6 get a single post by post id (GET based on post id from post table)
7 edit a post by post id (POST to post table)
8 delete a single post (DELETE from post table)
9 get all of today's posts (GET all from post table)
10 most recent 4 posts (GET 4 most recent posts from posts table)
11 get today's current winner (GET from post table)
#12 post daily image to table
#13 get current daily image from table
#14 cast a vote for a post
#15 retrive number of votes for a post
#16 get all past winners and images


'''


#1 Register New User
@api.route('/register', methods=['POST'])
def create_user():
    """
    [POST] /api/register
    """
    user = User()
    data = request.get_json()
    print(data)
    user.from_dict(data[0])
    user.password = generate_password_hash(user.password)
    user.save()
    return jsonify(user.to_dict())

#2 Login User
@api.route('/login', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({ 'token': token })

#3
@basic_auth.verify_password
def verify_password(username, password):
    u = User.query.filter_by(username=username).first()
    if u and check_password_hash(u.password, password):
        return u

#4
@token_auth.verify_token
def verify_token(token):
    if token:
        return User.check_token(token)
    return None

#5
@api.route('/post', methods=['POST']) 
@token_auth.login_required
def create_post():
    """
    [POST] /api/post
    """
    post = Post()
    user = token_auth.current_user()
    data = request.get_json()
    data['user_id'] = user.id
    data['votes'] = 0
    post.from_dict(data)
    post.save()
    return jsonify(post.to_dict())


# okay, so I could not tell you why, but the below function was preventing 
# us from being able to create a post. it was trying to run line 104
# with the params from the create_post function. commented for now


# #6 Get single post by post ID
# @api.route('/post/<int:id>', methods=['GET']) 
# @token_auth.verify_token
# def get_single_post(id):
#     """
#     [GET] /api/post/<int:id>
#     """
#     post = Post.query.get(id)
#     return jsonify(post.to_dict())


#7 edit an existing post by post id (POST to post table)
@api.route('/edit/<int:id>', methods=['POST']) 
@token_auth.login_required
def edit_single_post(id):
    """
    [GET] /api/edit/<int:id>
    """
    post = Post.query.get(id)
    user = token_auth.current_user()
    if post.user_id != user.id:
        return jsonify({'Error': 'You do not have access to update this post'}, 401)
    data = request.get_json()
    post.from_dict(data)
    post.save()
    return jsonify(post.to_dict())

#8
@api.route('/posts/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_post(id):
    """
    [DELETE] /api/posts/<id>
    """
    post = Post.query.get(id)
    post.delete()
    return jsonify([p.to_dict() for p in Post.query.all()])

#9 Get all of today's posts
@api.route('/today', methods=['GET']) 
def get_todays_posts():
    """
    [GET] /api/today
    """
    todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    todays_posts = Post.query.filter(Post.date_created >= todays_datetime).all()
    return jsonify([p.to_dict() for p in todays_posts])

#10 most recent 4 posts (GET 4 most recent posts from posts table)
@api.route('/recent', methods=['GET']) 
def recent_posts():
    """
    [GET] /api/recent
    """
    todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    recent = Post.query.filter(Post.date_created >= todays_datetime).order_by(desc('date_created')).limit(4)
    return jsonify([p.to_dict() for p in recent])

#11 get today's current winner
@api.route('/winner', methods=['GET']) 
def show_winner():
    """
    [GET] /api/winnder
    """
    recent = Post.query.order_by(desc('votes')).first()
    return jsonify(recent.to_dict())

#12 post daily image to table
@api.route('/dailyimage', methods=['POST'])
def set_image():
    outgoing_image = Daily_Image.query.order_by(desc('date_created')).first()
    outgoing_image.find_winner()
    db.session.add(outgoing_image)
    db.session.commit()
    image = Daily_Image()
    data = request.get_json()
    image.from_dict(data)
    image.save()
    return jsonify(image.to_dict())

#13 query daily_image
@api.route('/getdailyimage', methods=['GET'])
def get_image():
    # image = Daily_Image.query.order_by(desc('date_created')).first()
    # return jsonify(image.to_dict())
    todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    todays_image = Daily_Image.query.filter(Daily_Image.date_created >= todays_datetime).first()
    if todays_image is None:
        return jsonify({'image_url': 'None'})
    return jsonify(todays_image.to_dict())

#14 cast a vote
@api.route('/vote/<int:id>', methods=['POST']) 
@token_auth.login_required
def add_a_vote(id):
    """
    [GET] /api/castvote/<int:id>
    """
    post = Post.query.get(id)
    user = token_auth.current_user()
    now = datetime.utcnow()
    if user.last_voted < now - timedelta(seconds=86400):
        user.last_voted = datetime.utcnow()
        post.votes += 1
        user.save()
        post.save()
    return jsonify(post.to_dict())

#15 retrive number of votes for a post
@api.route('/getvote/<int:id>', methods=['GET']) 
def get_votes(id):
    """
    [GET] /api/getvote/<int:id>
    """
    post = Post.query.get(id)
    return jsonify(post.to_dict())

#16 query all winners and daily_images
@api.route('/getallwinners', methods=['GET'])
def get_allwinners():
    winners = Daily_Image.query.order_by(desc('date_created'))
    return jsonify([w.to_dict() for w in winners])
