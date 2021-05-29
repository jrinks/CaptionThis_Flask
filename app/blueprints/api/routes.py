from flask import request, jsonify
from . import bp as api
from app.blueprints.post.models import Post, Daily_Image
from .auth import token_auth, User

'''All api endpoint routes go here: 
1- get all of today's posts (GET all from post table)
2- get a single post by post id (GET based on post id from post table)
3- create a post (POST to post table)
4- update a post by post id (POST to post table)
5- delete a single post (DELETE from post table)
6- most recent 4 posts (GET 4 most recent posts from posts table)
7- add vote (POST to post table)  posts/vote/id
#### nah   8- remove vote (POST to post table) 
9- daily image add to table (POST from silly animal api to daily_imnage table)
10- pull daily image from daily image table
10- daily image get past winners (GET all from dialy_image)
11-get today's current winner (GET from post table)
12- create user Register (POST to user table)
13 login user (GET to user table)


'''


#1
@api.route('/posts', methods=['GET'])
#do we want @toekn auth here?
def get_todays_posts():
    """
    [GET] /api/posts
    """
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts]) #where posts.date_created is equal to today


#2
@api.route('/posts/<int:id>', methods=['GET'])
def get_single_post(id):
    """
    [GET] /api/posts
    """
    post = Post.query.get(id)
    return jsonify(post.to_dict())



#3
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

#4
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

#5
@api.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """
    [DELETE] /api/posts/<id>
    """
    post = Post.query.get(id)
    post.delete()
    return jsonify([p.to_dict() for p in Post.query.all()])

#6



#12
