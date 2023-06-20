from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        user_with_email = User.query.filter_by(email=email).first()
        user_with_username = User.query.filter_by(username=username).first()

        if user_with_email:
            flash('Email already exists.')
            return redirect(url_for('auth.signup'))
        if user_with_username:
            flash('Username already exists.')
            return redirect(url_for('auth.signup'))

        new_user = User(email=email, username=username,
                        password=generate_password_hash(password))

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html')


@bp.route('/login/')
def login():
    return render_template('auth/login.html')


@bp.route('/logout/')
def logout():
    return render_template('auth/logout.html')
