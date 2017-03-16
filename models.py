from flask_sqlalchemy import SQLAlchemy
from main import app

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.String(45), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    posts = db.relationship(
        'Post',
        backref='users',
        lazy='dynamic')

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return "<Model User '{}'>".format(self.username)


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.String(45), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime)

    user_id = db.Column(db.String(45), db.ForeignKey('user.id'))

    comments = db.relationship(
        'Comment',
        backref='posts',
        lazy='dynamic')

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Model Post `{}`>".format(self.title)


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.String(45), db.ForeignKey('posts.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Model Comment `{}`>'.format(self.name)
