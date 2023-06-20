from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __str__(self):
        return self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey(
                            'user.id', ondelete='CASCADE', onupdate='CASCADE'),
                        nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __str(self):
        return self.title
