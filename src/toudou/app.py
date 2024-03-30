from flask import Flask, render_template
from toudou import config

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

def create_app():
    app = Flask(__name__)

    app.secret_key = config['FLASK_SECRET_KEY']

    from toudou.views.web import web_ui
    app.register_blueprint(web_ui)

    return app

users = {
    "admin": { 
        "password" : generate_password_hash("admin"), 
        "role" : "admin"
    },
    "user": {
        "password" : generate_password_hash("user"),
        "role" : "user"
    }
}

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users[username]["password"], password):
        return username

@auth.get_user_roles
def get_user_roles(username):
    return [users[username]["role"]] if username in users else [] 
        
    

@auth.error_handler
def auth_error(status):
    return "Your are a user which means you are in read-only state ", status