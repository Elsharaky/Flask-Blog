from flaskblog import db,login_manager
from datetime import datetime
from flask_login import UserMixin # Used to add more fields to the user table (is_authenticated,is_active,is_anonymous,get_id())


# The following function is mandatory for the flask-login extention to work!
@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    profile_img = db.Column(db.String(20),default='default.jpg',nullable=False)
    posts = db.relationship('Post',backref='author')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(250),nullable=False)
    content = db.Column(db.Text,nullable=False)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date}')"
