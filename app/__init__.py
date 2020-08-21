from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)

app.config.from_object('config')

# Define MongoDB instance
db = MongoEngine(app)

# Bootstrap
bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login' # Controller

@app.errorhandler(404)
def notfound(error):
    return render_template('404.html'), 404

# Project modules
from app.auth.forms import LoginForm, RegisterForm
from app.auth.view import auth as auth_module
from app.api.view import api as api_module

app.register_blueprint(auth_module)
app.register_blueprint(api_module)
