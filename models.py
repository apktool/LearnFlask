from flask_script import SQLAlchemy
from main import app

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Colume(db.String(45), primary_key=True)
    username = db.Colume(db.String(255))
    password = db.Colume(db.String(255))

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "<Model User '{}'>".format(self.username)
