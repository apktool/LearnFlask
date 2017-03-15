from flask_sqlalchemy import SQLAlchemy
from main import app

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.String(45), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return "<Model User '{}'>".format(self.username)
