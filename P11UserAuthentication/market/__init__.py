from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '145088f4b2c1fbd045479d3d'
db = SQLAlchemy(app)
# store password as hash password
bcrypt= Bcrypt(app)
login_manager=LoginManager(app)
from market import routes