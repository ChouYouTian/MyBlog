from flask import render_template, url_for, redirect, request, session, flash,Blueprint
from flask_login import current_user,login_required
from .forms import PostForm,TestForm
from myweb.models import Post,Draft
from myweb import db,app
from PIL import Image
import os
import secrets


posts=Blueprint('posts',__name__)



@posts.route('/post')
@login_required
def post(path=''):
    myposts=Post.query.filter_by(user_id=current_user.id)
    print(myposts)
    
    return render_template('post.html',posts=myposts)

@posts.route('/post/new',methods=["POST", "GET"])
@login_required 
def new_post():
    if request.method=='POST':
        content=request.form.get('content')
        title=request.form.get('title')
        type=request.form.get('type')
        print(type,title)
        
        if type=='post':
            add_post= Post(title=title,content=content,author=current_user)
            db.session.add(add_post)
            db.session.commit()
        
            flash('posted','success')
        elif type=='draft':
            add_draft= Draft(title=title,content=content,author=current_user)
            db.session.add(add_draft)

            db.session.commit()
            flash('saved','success')

        return redirect(url_for('main.home'))
    
    return render_template('new_post.html')



@posts.route('/draft')
def draft():
    return render_template('draft.html')





@posts.route('/test',methods=["Get","POST"])
def test():

    if request.method=='POST':
        content=request.get_json()
        content=request.form.get('data')
        print(content)
        
        return redirect(url_for('main.home'))
    else:
        return render_template('test.html')


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


# @posts.route('/summer',methods=["POST","GET"])
# def summer():
#     if request.method=='POST':
#         content=request.form.get('content')
#         print(content)
#         print(request.form.get('type'))
#         flash('posted','success')
        
#         return redirect(url_for('main.home'))
    
#     return render_template('summernote.html')

