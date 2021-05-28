from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.blueprints.auth.models import User
from werkzeug.security import check_password_hash

####### I did not chnage anything on this page, this is from Brian's project.  

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password):
    u = User.query.filter_by(username=username).first()
    if u and check_password_hash(u.password, password):
        return u


@token_auth.verify_token
def verify_token(token):
    if token:
        return User.check_token(token)
    return None