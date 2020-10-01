from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import config

app = Flask(__name__)

app.config['SECRET_KEY'] = config.secret['secret_key']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

login_manager = LoginManager(app)
db = SQLAlchemy(app)

from comic_wishlist import routes