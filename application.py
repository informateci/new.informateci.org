__author__ = 'mandrake'
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)

# Initializing login manager
login_manager = LoginManager()
login_manager.init_app(app)