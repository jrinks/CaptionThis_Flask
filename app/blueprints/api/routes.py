from flask import request, jsonify
from . import bp as api
from app.blueprints.post.models import Post, Daily_Image
from .auth import token_auth, User

'''All api endpoint routes go here: 

- Register (POST to user table)
- login user (GET to user table)
- get all of today's posts (GET all from post table)
- get a single post by post id (GET based on post id from post table)
- create a post (POST to post table)
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
    user.save()
    return jsonify(user.to_dict())



#
@api.route('/posts', methods=['GET'])
#do we want @toekn auth here?
def get_todays_posts():
    """
    [GET] /api/posts
    """
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts]) #where posts.date_created is equal to today


#
@api.route('/posts/<int:id>', methods=['GET'])
def get_single_post(id):
    """
    [GET] /api/posts
    """
    post = Post.query.get(id)
    return jsonify(post.to_dict())



#
@api.route('/posts', methods=['POST'])
@token_auth.login_required
def create_post():
    """
    [POST] /api/posts
    """
    post = Post()
    user = token_auth.current_user()
    data = request.get_json()
    data['user_id'] = user.id
    post.from_dict(data)
    post.save()
    return jsonify(post.to_dict())

#
@api.route('/posts/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_post(id):
    """
    [PUT] /api/posts/<id>
    """
    post = Post.query.get(id)
    user = token_auth.current_user()
    print(user)
    if post.user_id != user.id:
        print("here")
        return jsonify({'Error': 'You do not have access to update this post'}, 401)
    data = request.get_json()
    post.from_dict(data)
    post.save()
    return jsonify(post.to_dict())

#
@api.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """
    [DELETE] /api/posts/<id>
    """
    post = Post.query.get(id)
    post.delete()
    return jsonify([p.to_dict() for p in Post.query.all()])

