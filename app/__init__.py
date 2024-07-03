import os

from flask import Flask
from app.extensions import engine, Base, Session
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

from app.extensions import engine, Base, Session

login_manager = LoginManager(app)

from app import routes, models
