from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app import models, app

manager = Manager(app)
manager.add_command('server', Server(host='127.0.0.1', port=8089))
migrate = Migrate(app, models.db)
manager.add_command("db", MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app,
                db=models.db,
                User=models.User,
                Post=models.Post,
                Comment=models.Comment,
                Tag=models.Tag,
                Server=Server)


if __name__ == '__main__':
    manager.run()


'''
python3 manage.py shell
>>> db.create_all()
'''
