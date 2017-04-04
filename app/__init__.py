from flask import Flask, redirect, url_for
from config import dev_config, basic_config
from .models import db
from .controllers import blog

app = Flask(__name__)
app.config.from_object(dev_config)
app.config.from_object(basic_config)

db.init_app(app)

@app.route('/')
def index():
    return redirect(url_for('blog.home'))

app.register_blueprint(blog.blog_blueprint)

if __name__ == '__main__':
    app.run()
