from flask import Flask
from config import dev_config

app = Flask(__name__)
app.config.from_object(dev_config)


@app.route('/')
def home():
    return '<h1>hello world</h1>'


if __name__ == '__main__':
    app.run()
