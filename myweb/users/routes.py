from flask import Blueprint,render_template,render_template, url_for, redirect, request, session, flash,abort
from flask_login import login_user,logout_user,current_user,login_required
from .forms import LoginForm,UpdateAccountForm,SignUpForm
from .utils import update_account,sign_up_user,check_user

users=Blueprint('users',__name__)


@users.route('/login', methods=["POST", "GET"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user=check_user(form.email_name.data,form.password.data)
        
        if user:
            login_user(user,remember=form.remeber.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else  redirect(url_for('main.home'))
        
        else:
            flash('Failed to login . Please check email and password', 'danger')
            return render_template('users/login.html', form=form),401
    
    elif request.method=="GET":
        return render_template('users/login.html', form=form)
    
    else:
        flash('Failed to login . Please check email and password', 'danger')
        return render_template('users/login.html', form=form),401



@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))
    


@users.route('/signup', methods=["POST", "GET"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        sign_up_user(form.username.data,form.email.data,form.password.data)
        flash(f'Account created for {form.username.data}! You can login now', 'success')
        return redirect(url_for('users.login'))
    elif request.path=='GET':
        return render_template('users/signup.html', form=form)
    else:
        return render_template('users/signup.html', form=form),400




@users.route('/account',methods=["POST", "GET"])
@login_required
def account():
    form=UpdateAccountForm()

    if form.validate_on_submit():
        update_account(form.username.data,form.email.data,form.picture.data)
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))

    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
        imagefile=url_for('static',filename='picture/'+current_user.image_file)
        return render_template("users/account.html",image_file=imagefile,form=form)
    
    else:
        imagefile=url_for('static',filename='picture/'+current_user.image_file)
        return render_template("users/account.html",image_file=imagefile,form=form),400

@users.route('/user')
def user():
    if 'user' in session:
        user = session["user"]
        return render_template("users/user.html", user=user)
    else:
        return redirect(url_for('users.login'))

