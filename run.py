from app import create_app, db
from app.blueprints.api.models import User
from app.blueprints.api.models import Post
from app.blueprints.api.models import Daily_Image


app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Daily_Image': Daily_Image}