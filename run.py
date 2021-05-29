from app import create_app, db
from app.blueprints.auth.models import User
from app.blueprints.post.models import Post
from app.blueprints.post.models import Daily_Image


app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Daily_Image': Daily_Image}