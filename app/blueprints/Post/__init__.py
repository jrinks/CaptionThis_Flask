from flask import Blueprint

bp = Blueprint('post', __name__, url_prefix='/post')

from . import routes, models