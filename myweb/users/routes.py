from flask import Blueprint,render_template,render_template, url_for, redirect, request, session, flash
from myweb import db,bcrypt
from flask_login import login_user,logout_user,current_user,login_required
from myweb.models import User
from .forms import LoginForm,UpdateAccountForm,SignUpForm
from .utils import save_picture


users=Blueprint('users',__name__)

@users.route('/login', methods=["POST", "GET"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remeber.data)

            next_page=request.args.get('next')

            return redirect(next_page) if next_page else  redirect(url_for('main.home'))
        else:
            flash('Failed to login . Please check email and password', 'danger')
    return render_template('login.html', form=form)



@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))
    


@users.route('/signup', methods=["POST", "GET"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        hashedPassword=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashedPassword)

        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data}! You can login now', 'success')
        return redirect(url_for('users.login'))

    return render_template('signup.html', form=form)


@users.route('/user')
def user():
    if 'user' in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        return render_template("login.html")






@users.route('/account',methods=["POST", "GET"])
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
        return redirect(url_for('users.account'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email


    imagefile=url_for('static',filename='picture/'+current_user.image_file)
    return render_template("account.html",image_file=imagefile,form=form)
