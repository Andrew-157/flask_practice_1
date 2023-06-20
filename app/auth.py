from flask import Blueprint, render_template

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login/')
def login():
    return render_template('auth/login.html')


@bp.route('/signup/')
def signup():
    return render_template('auth/signup.html')


@bp.route('/logout/')
def logout():
    return render_template('auth/logout.html')
