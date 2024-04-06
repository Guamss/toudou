from flask import Flask, render_template
from toudou import config, models

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from toudou.views.wtf import DeleteToudouForm

def create_app():
    app = Flask(__name__)

    app.secret_key = config['FLASK_SECRET_KEY']
    models.createTable()
    from toudou.views.api import api, api_spec
    from toudou.views.web import web_ui
    app.register_blueprint(web_ui)
    app.register_blueprint(api)
    api_spec.register(app)

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
    return render_template("display.html", todos=models.getToudous(), form=DeleteToudouForm()), status