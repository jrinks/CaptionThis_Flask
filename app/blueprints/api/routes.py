from datetime import datetime
from sqlite3 import Timestamp
from flask import request, jsonify
from flask_login import current_user
from app.blueprints.api.models import Post, User, UserMixin, Daily_Image
from app import db
from . import bp as api
from werkzeug.security import check_password_hash, generate_password_hash
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

'''All api endpoint routes go here: 

1 Register (POST to user table)
2 login user (GET to user table)
3 Basic Auth
4 Token Auth
5 create a post (POST to post table)
6 get all of today's posts (GET all from post table)
- get a single post by post id (GET based on post id from post table)

- update a post by post id (POST to post table)
- delete a single post (DELETE from post table)
- most recent 4 posts (GET 4 most recent posts from posts table)
- add vote (POST to post table)  posts/vote/id
- daily image add to table (POST from silly animal api to daily_imnage table)
- pull daily image from daily image table
- daily image get past winners (GET all from dialy_image)
- get today's current winner (GET from post table)



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


#6
@api.route('/today', methods=['GET']) 
@token_auth.login_required
def get_todays_posts():
    """
    [GET] /api/today
    """
    todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    todays_posts = Post.query.filter(Post.date_created >= todays_datetime).all()
    return jsonify([p.to_dict() for p in todays_posts])

#7
@api.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """
    [DELETE] /api/posts/<id>
    """
    post = Post.query.get(id)
    post.delete()
    return jsonify([p.to_dict() for p in Post.query.all()])



# @api.route('/tokens', methods=['POST'])
# @basic_auth.login_required
# def get_token():
#     token = basic_auth.current_user().get_token()
#     db.session.commit()
#     return jsonify({ 'token': token })

# #
# @api.route('/posts', methods=['GET'])
# #do we want @toekn auth here?
# def get_todays_posts():
#     """
#     [GET] /api/posts
#     """
#     posts = Post.query.all()
#     return jsonify([p.to_dict() for p in posts]) #where posts.date_created is equal to today


# #
# @api.route('/posts/<int:id>', methods=['GET'])
# def get_single_post(id):
#     """
#     [GET] /api/posts
#     """
#     post = Post.query.get(id)
#     return jsonify(post.to_dict())



# #
# @api.route('/posts', methods=['POST'])
# @token_auth.login_required
# def create_post():
#     """
#     [POST] /api/posts
#     """
#     post = Post()
#     user = token_auth.current_user()
#     data = request.get_json()
#     data['user_id'] = user.id
#     post.from_dict(data)
#     post.save()
#     return jsonify(post.to_dict())

# #
# @api.route('/posts/<int:id>', methods=['PUT'])
# @token_auth.login_required
# def update_post(id):
#     """
#     [PUT] /api/posts/<id>
#     """
#     post = Post.query.get(id)
#     user = token_auth.current_user()
#     print(user)
#     if post.user_id != user.id:
#         print("here")
#         return jsonify({'Error': 'You do not have access to update this post'}, 401)
#     data = request.get_json()
#     post.from_dict(data)
#     post.save()
#     return jsonify(post.to_dict())





