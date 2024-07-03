import os

from flask import Flask
from app.extensions import engine, Base, Session
from flask_login import LoginManager
from app.config import config
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# app.config.from_object(config[app.config['FLASK_ENV']])

from app.extensions import engine, Base, Session

login_manager = LoginManager(app)

from app import routes, models
