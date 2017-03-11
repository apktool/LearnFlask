from flask_script import Manager, Server
import main

manger = Manager(main.app)
manger.add_command('server', Server())


@manger.shell
def make_shell_context():
    return dict(app=main.app)


if __name__ == '__main__':
    manger.run()
