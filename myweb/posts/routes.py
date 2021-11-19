from flask import blueprints, render_template, url_for, redirect, request, session, flash,Blueprint
from flask_login import login_user,logout_user,current_user,login_required
from .forms import PostForm,TestForm
from myweb.models import Post,Draft
from myweb import db,app
from PIL import Image
import os
import secrets


posts=Blueprint('posts',__name__)



@posts.route('/post')
def post(path=''):
    
    return render_template('post.html',txt=path)

@posts.route('/post/new',methods=["POST", "GET"])
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


@posts.route('/draft')
def draft():
    return render_template('draft.html')





@posts.route('/test',methods=["Get","POST"])
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


@posts.route('/saveimg',methods=["POST"])
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

    