from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import Post
from . import db

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('main/index.html')


@bp.route('/profile/')
@login_required
def profile():
    return render_template('main/profile.html', username=current_user.username)


@bp.route('/create_post/', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        errors = False

        if not title:
            flash('Title is required to create a post.')
            errors = True
        if not content:
            flash('Content is required to create a post.')
            errors = True

        if errors:
            return redirect(url_for('main.create_post'))

        post = Post(
            title=title,
            content=content,
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()

        flash('You successfully published new post.')
        return redirect(url_for('main.profile'))

    return render_template('main/create.html')
