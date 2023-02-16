from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,PasswordField,validators,TextAreaField
from flask_wtf.file import FileField,FileAllowed,FileSize
from flaskblog.models import User
from flask_login import current_user

class RegisterationForm(FlaskForm):
    username = StringField(label='Username',validators=[validators.DataRequired(),validators.Length(min=6,max=20)])

    email = StringField(label='Email',validators=[validators.DataRequired(),validators.Email()])

    password = PasswordField(label='Password',validators=[validators.DataRequired(),validators.Length(min=8,max=50)])

    rePassword = PasswordField(label='Confirm password',validators=[validators.DataRequired(),validators.EqualTo(fieldname='password')])

    submit = SubmitField(label='Sign Up')

    # This is a custom validation
    def validate_username(self,username):
        if User.query.filter_by(username=username.data).first():
            raise validators.ValidationError('This username already exists!')

    def validate_email(self,email):
        if User.query.filter_by(email=email.data).first():
            raise validators.ValidationError('This E-mail already exists!')


class LoginForm(FlaskForm):
    email = StringField(label='Email',validators=[validators.DataRequired(),validators.Email()])

    password = PasswordField(label='Password',validators=[validators.DataRequired(),validators.Length(min=8,max=50)])

    remember = BooleanField(label='Remeber Me')

    submit = SubmitField(label='Login')

class AccountForm(FlaskForm):
    username = StringField(label='Username',validators=[validators.DataRequired(),validators.Length(min=6,max=20)])

    email = StringField(label='Email',validators=[validators.DataRequired(),validators.Email()])

    # You should validate the uploaded file much more using python-magic lib.
    file = FileField(label='Upload your image.',validators=[FileAllowed({'png','jpg','jpeg','gif'}),FileSize(max_size=2*1024*1024)])

    submit = SubmitField(label='Update')

    # This is a custom validation
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user and user.username != current_user.username:
            raise validators.ValidationError('This username already exists!')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user and user.email != current_user.email:
            raise validators.ValidationError('This E-mail already exists!')


class CreatePostForm(FlaskForm):
    title = StringField(label='Title',validators=[validators.DataRequired()])

    content = TextAreaField(label='Content',validators=[validators.DataRequired()])

    submit = SubmitField(label='Post')

class UpdatePostForm(FlaskForm):
    title = StringField(label='Title',validators=[validators.DataRequired()])

    content = TextAreaField(label='Content',validators=[validators.DataRequired()])

    submit = SubmitField(label='Update')

    