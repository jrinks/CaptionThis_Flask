from . import bp as blog
from app import db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .forms import PostForm, DeletePostForm
from .models import Post


@blog.route('/createpost', methods=['GET', 'POST'])
@login_required
def createpost():
    title = 'CREATE POST'
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():
        post_title = form.title.data
        post_body = form.body.data
        user_id = current_user.id

        new_post = Post(post_title, post_body, user_id)

        db.session.add(new_post)
        db.session.commit()

        flash(f"You have created a post: {post_title}", 'info')

        return redirect(url_for('main.index'))

    return render_template('createpost.html', title=title, form=form)


@blog.route('/myposts')
@login_required
def myposts():
    title = 'MY POSTS'
    posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template('myposts.html', title=title, posts=posts)


@blog.route('/posts/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    context = {
        'post': post,
        'title': post.title,
        'form': DeletePostForm()
    }
    return render_template('post_detail.html', **context)


@blog.route('/posts/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    title = f'UPDATE {post.title}'
    if post.author.id != current_user.id:
        flash("You cannot update another user's post. Who do you think you are?", "warning")
        return redirect(url_for('blog.myposts'))
    update_form = PostForm()
    if request.method == 'POST' and update_form.validate_on_submit():
        post_title = update_form.title.data
        post_body = update_form.body.data

        post.title = post_title
        post.body = post_body

        db.session.commit()

        return redirect(url_for('blog.post_detail', post_id=post.id))

    return render_template('post_update.html', title=title, post=post, form=update_form)


@blog.route('/posts/delete/<int:post_id>', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.id != current_user.id:
        flash("You cannot delete another user's post. Who do you think you are?", "warning")
        return redirect(url_for('blog.myposts'))
    form = DeletePostForm()
    if form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()
        flash(f'{post.title} has been deleted', 'info')
        return redirect(url_for('blog.myposts'))
    return redirect(url_for('main.index'))