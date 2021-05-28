from flask import request, jsonify
from . import bp as api
from app.blueprints.blog.models import Post
from .auth import token_auth
from .models import Product


@api.route('/posts', methods=['GET'])
def get_posts():
    """
    [GET] /api/posts
    """
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])


@api.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    """
    [GET] /api/posts
    """
    post = Post.query.get(id)
    return jsonify(post.to_dict())


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


@api.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """
    [DELETE] /api/posts/<id>
    """
    post = Post.query.get(id)
    post.delete()
    return jsonify([p.to_dict() for p in Post.query.all()])


@api.route('/products')
def products():
    """
    [GET] /api/products
    """
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])


@api.route('/products/<int:id>')
def single_product(id):
    """
    [GET] /api/products/<id>
    """
    p = Product.query.get_or_404(id)
    return jsonify(p.to_dict())