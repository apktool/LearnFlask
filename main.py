from flask import Flask
from config import dev_config

app = Flask(__name__)
app.config.from_object(dev_config)

views = __import__('views')

if __name__ == '__main__':
    app.run()
