import os
import secrets
from PIL import Image
from flask import render_template, url_for, redirect, request, session, flash
from myweb import app,db,bcrypt
from myweb.forms import SignUpForm, LoginForm,UpdateAccountForm,PostForm,TestForm
from myweb.models import User,Post,Draft
from flask_login import login_user,logout_user,current_user,login_required



@app.route('/')
@app.route('/home')
def home():
    posts=Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/login', methods=["POST", "GET"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remeber.data)

            next_page=request.args.get('next')

            return redirect(next_page) if next_page else  redirect(url_for('home'))
        else:
            flash('Failed to login . Please check email and password', 'danger')
    return render_template('login.html', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
    


@app.route('/signup', methods=["POST", "GET"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        hashedPassword=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashedPassword)

        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data}! You can login now', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


@app.route('/user')
def user():
    if 'user' in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        return render_template("login.html")


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/picture', picture_fn)
    
    # resize the picture
    output_size = (125, 125)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



@app.route('/account',methods=["POST", "GET"])
@login_required
def account():
    form=UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picturefile=save_picture(form.picture.data)
            current_user.image_file=picturefile
        
        current_user.username=form.username.data
        current_user.email=form.email.data

        db.session.commit()

        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email


    imagefile=url_for('static',filename='picture/'+current_user.image_file)
    return render_template("account.html",image_file=imagefile,form=form)

@app.route('/post')
def post(path=''):
    
    return render_template('post.html',txt=path)

@app.route('/post/new',methods=["POST", "GET"])
@login_required 
def new_post():
    form=PostForm()

    if form.validate_on_submit():
        if form.submit.data:
            add_post= Post(title=form.title.data,content=form.content.data,author=current_user)
            db.session.add(add_post)
            db.session.commit()
            
        elif form.save_draft.data:
            add_draft= Draft(title=form.title.data,content=form.content.data,author=current_user)
            db.session.add(add_draft)

            db.session.commit()
        
        return redirect(url_for('home'))

    return render_template('new_post.html',form=form)


@app.route('/draft')
def draft():
    return render_template('draft.html')





@app.route('/test',methods=["Get","POST"])
def test():
    form=TestForm()
    if form.validate_on_submit():
        print('get submit')
    
    if request.method=='POST':
        content=request.get_json()
        print(content)
        
        return redirect(url_for('home'))
    else:
        return render_template('test.html',form=form)


@app.route('/saveimg',methods=["POST"])
def saveimg():
    if request.method=='POST':

        form_picture=request.files.get('image')

        
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(app.root_path, 'static/picture/temp', picture_fn)

        print(picture_path)

        i = Image.open(form_picture)
        i.save(picture_path)

        return 'static/picture/temp/'+picture_fn

    

