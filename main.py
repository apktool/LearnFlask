from flask import Flask
from config import dev_config, basic_config
import wt_forms

app = Flask(__name__)
app.config.from_object(dev_config)
app.config.from_object(basic_config)

views = __import__('views')

if __name__ == '__main__':
    app.run()
