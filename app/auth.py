from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        if not username:
            flash('Username is required')
            return redirect(url_for('auth.signup'))
        elif not email:
            flash('Email is required.')
            return redirect(url_for('auth.signup'))
        elif not password:
            flash('Password is required.')
            return redirect(url_for('auth.signup'))

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


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = True if request.form.get('remember') else False

        if not email:
            flash('Enter your email to login.')
            return redirect(url_for('auth.login'))
        elif not password:
            flash('Enter your password to login.')
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(email=email).first()

        if not user:
            flash('Email was not found, try again.')
            return redirect(url_for('auth.login'))
        elif not check_password_hash(user.password, password):
            flash('Password does not match, try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))

    return render_template('auth/login.html')


@bp.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/change_profile/', methods=['GET', 'POST'])
@login_required
def change_profile():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        errors = False

        if not email:
            flash('Enter your new email.')
            errors = True
        if not username:
            flash('Enter your new username.')
            errors = True
        user_with_email = User.query.filter_by(email=email).first()
        user_with_username = User.query.filter_by(username=username).first()

        if user_with_email and (user_with_email != current_user):
            flash('User with this email already exists.')
            errors = True
        if user_with_username and (user_with_username != current_user):
            flash('User with this username already exists.')
            errors = True

        if errors:
            return redirect(url_for('auth.change_profile'))

        current_user.username = username
        current_user.email = email
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('auth/change_profile.html')
