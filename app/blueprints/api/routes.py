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
7 get a single post by post id (GET based on post id from post table)
8 update a post by post id (POST to post table)
9 delete a single post (DELETE from post table)
10 most recent 4 posts (GET 4 most recent posts from posts table)
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
@token_auth.verify_token
def create_post():
    """
    [POST] /api/post
    """
    post = Post()
    data = request.get_json()
    print("post data received")
    post.from_dict(data)
    post.votes = 0
    #post.user_id = current_user[user_id]
    post.save()
    return jsonify(post.to_dict())


#6 Get all of today's posts
@api.route('/today', methods=['GET']) 
@token_auth.verify_token
def get_todays_posts():
    """
    [GET] /api/today
    """
    print("todays posts go here")
    todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    todays_posts = Post.query.filter(Post.date_created >= todays_datetime).all()
    return jsonify([p.to_dict() for p in todays_posts])

#7 Get single post by post ID
@api.route('/post/<int:id>', methods=['GET']) 
@token_auth.verify_token
def get_single_post(id):
    """
    [GET] /api/post/<int:id>
    """
    post = Post.query.get(id)
    return jsonify(post.to_dict())


#8 edit an existing post by post id (POST to post table)
@api.route('/edit/<int:id>', methods=['GET']) 
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

#9 delete a post
@api.route('/delete/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_post(id):
    """
    [DELETE] /api/post/delete/<id>
    """
    post = Post.query.get(id)
    post.delete()
    return jsonify([p.to_dict() for p in Post.query.all()])

#10 most recent 4 posts (GET 4 most recent posts from posts table)
@api.route('/recent', methods=['GET']) 
def recent_posts():
    """
    [GET] /api/recent
    """
    recent = Post.query.order_by('date_created').limit(4)
    return jsonify([p.to_dict() for p in recent])

#10 get today's current winnder
@api.route('/winner', methods=['GET']) 
def show_winner():
    """
    [GET] /api/winnder
    """
    recent = Post.query.order_by('votes').limit(1)
    return jsonify([p.to_dict() for p in recent])




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

# #
# @api.route('/posts/<int:id>', methods=['DELETE'])
# def delete_post(id):
#     """
#     [DELETE] /api/posts/<id>
#     """
#     post = Post.query.get(id)
#     post.delete()
#     return jsonify([p.to_dict() for p in Post.query.all()])




