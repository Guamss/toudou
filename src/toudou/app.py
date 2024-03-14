from flask import Flask
from toudou import config

def create_app():
    app = Flask(__name__)

    app.secret_key = config['FLASK_SECRET_KEY']
    from toudou.views import web_ui
    app.register_blueprint(web_ui)

    return app