from flask_script import Manager, Server
import main
import models

manger = Manager(main.app)
manger.add_command('server', Server())


@manger.shell
def make_shell_context():
    return dict(app=main.app,
                db=models.db,
                User=models.User,
                Post=models.Post,
                Comment=models.Comment,
                Tag=models.Tag)


if __name__ == '__main__':
    manger.run()


'''
python3 manage.py shell
>>> db.create_all()
'''
