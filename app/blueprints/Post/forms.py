from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    post_body = StringField('Post Body')
    image_url = StringField('Image URL')
    submit = SubmitField()


class DeletePostForm(FlaskForm):
    submit = SubmitField()