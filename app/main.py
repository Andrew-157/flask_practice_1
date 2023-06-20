from flask import Blueprint

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return 'Index page'


@bp.route('/profile/')
def profile():
    return 'Your profile'
