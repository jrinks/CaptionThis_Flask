from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_cors import CORS
from config import Config


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()
cors = CORS()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    cors.init_app(app)

    login.login_view = 'auth.login'
    login.login_message_category = 'danger'

    with app.app_context():
        from app.blueprints.auth import bp as auth
        app.register_blueprint(auth)

        from app.blueprints.post import bp as post
        app.register_blueprint(post)

       
        from app.blueprints.api import bp as api
        app.register_blueprint(api)

    return app
