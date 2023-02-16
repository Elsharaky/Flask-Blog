from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from secrets import token_hex

app = Flask(__name__)
app.config['SECRET_KEY'] = token_hex(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../flaskblog/blog.db'
app.app_context().push()


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.session_protection = 'strong' # to protect the session cookie from being stolen
login_manager.login_view = 'login' # where to redirect the user if the login is required
login_manager.login_message_category = 'info'
login_manager.login_message = "Should be logged in first!"


from flaskblog import routes