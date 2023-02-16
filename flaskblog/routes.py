from flask import render_template,redirect,url_for,flash,request,abort
from flaskblog.forms import RegisterationForm,LoginForm,AccountForm,CreatePostForm,UpdatePostForm
from flaskblog import app,bcrypt,db
from flaskblog.models import User,Post
from flask_login import login_user,logout_user,login_required,current_user
from secrets import token_hex
import os
from PIL import Image

@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('index.html',posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',title='About')

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('The account created successfully!','success')
        return redirect(url_for('login'))
    
    return render_template('register.html',title='Register',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            flash('Logged In successfully!!','success')
            # if the next parameter exist it will redirect the user to it's path.
            # the next parameter exists when the user try to access path that require login.
            return redirect('/' + request.args.get('next')[1:]) if request.args.get('next') else redirect(url_for('home'))
        else:
            flash('Invalid email or password!','danger')
    return render_template('login.html',title='Login',form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!','success')
    return redirect(url_for('home'))

def save_img(form_img):
    while 1:
        img_name = token_hex(8)
        _,ext = os.path.splitext(form_img.filename)
        if not User.query.filter_by(profile_img=img_name+ext).first():
            break
    img_name = img_name + ext

    # We do this to make the image size smaller.
    new_img = Image.open(form_img)
    new_img.thumbnail((125,125))

    new_img.save(os.path.join(app.root_path,'static/images',img_name))
    return img_name

@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = AccountForm()
    img = current_user.profile_img
    if form.validate_on_submit():
        if form.username.data != current_user.username or form.email.data != current_user.email: 
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Account information updated sucessfully!','success')
        elif form.file.data:
            img_name = save_img(form.file.data)
            if current_user.profile_img != 'default.jpg':
                os.remove(os.path.join(app.root_path,'static/images',current_user.profile_img))
            current_user.profile_img = img_name
            db.session.commit()
            img = current_user.profile_img
            flash('Your image updated successfully!','success')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html',title='Account',form=form,img=img)


@app.route('/create_post',methods=['GET','POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post uploaded successfully!','success')
        return redirect(url_for('home'))
    return render_template('create_post.html',title='Create Post',form=form)

@app.route('/posts')
def post():
    post = Post.query.get(request.args.get('post'))
    return render_template('posts.html',title=f'{post.author.username} Post',post=post) if post else abort(404)


@app.route('/posts/update',methods=['GET','POST'])
@login_required
def update_post():
    post = Post.query.get(request.args.get('post'))
    if post and post.author == current_user:
        form = UpdatePostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash('Post updated successfully!','success')
            return redirect(url_for('home'))
        elif request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content
        return render_template('update_post.html',title='Update post',form=form)
    return abort(404)

@app.route('/posts/delete')
@login_required
def delete_post():
    post = Post.query.get(request.args.get('post'))
    if post and post.author == current_user:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!','success')
        return redirect(url_for('home'))
    return abort(404)

