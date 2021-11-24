
from flask import render_template, url_for, redirect, request, session, flash,Blueprint,abort
from flask_login import current_user,login_required
from .forms import PostForm,TestForm,UpdatePostForm
from myweb.models import Post,Draft
from myweb import db,app
from .util import saveimg_in_sever,get_post,save_post,post_draft


posts=Blueprint('posts',__name__)



@posts.route('/post')
@login_required
def post():
    my_posts=Post.query.filter_by(user_id=current_user.id)
    my_drafts=Draft.query.filter_by(user_id=current_user.id)
    
    return render_template('post.html',posts=my_posts,drafts=my_drafts)

@posts.route('/post/<int:post_id>')
def post_id(post_id):
    post=Post.query.filter_by(id=post_id).first()

    return render_template('post_id.html',post=post)


@posts.route('/post_new',methods=["POST", "GET"])
@login_required 
def post_new():
    if request.method=='POST':
        content=request.form.get('content')
        title=request.form.get('title')
        type=request.form.get('type')
        # print(type,title)
        
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

@posts.route('/editor',methods=["POST", "GET"])
@login_required
def editor():
    
    form=UpdatePostForm()
    if form.validate_on_submit():
        post=get_post(form.id.data,form.post_type.data)
        if form.save.data:
            save_post(post,form.title.data,form.content.data)
        elif form.post.data:
            post_draft(post,form.title.data,form.content.data)

        flash('Your post has been updated!', 'success')

        return redirect(url_for('main.home'))

    elif request.method=='GET':
        id=request.args.get('id')
        post_type=request.args.get('type')
        # print(id,type(post_type))

        post=get_post(id,post_type)

        if post:
            form.id.data=id
            form.post_type.data=post_type
            form.content.data=post.content
            form.title.data=post.title


    return render_template('test.html',form=form)





@posts.route('/saveimg',methods=["POST"])
def saveimg():
    if request.method=='POST':
        form_picture=request.files.get('image')
        return saveimg_in_sever(form_picture)


@posts.route('/summer',methods=["POST","GET"])
def summer():
    if request.method=='POST':
        content=request.form.get('content')
        # print(content)
    return render_template('summernote.html')



@posts.route('/test',methods=["Get","POST"])
def test():

    form=UpdatePostForm()
    if form.validate_on_submit():
        post=get_post(form.id.data,form.post_type.data)
        if form.save.data:
            save_post(post,form.title.data,form.content.data)
        elif form.post.data:
            post_draft(post,form.title.data,form.content.data)

        flash('Your post has been updated!', 'success')

        return redirect(url_for('main.home'))

    elif request.method=='GET':
        id=request.args.get('id')
        post_type=request.args.get('type')
        # print(id,type(post_type))

        post=get_post(id,post_type)

        if post:
            form.id.data=id
            form.post_type.data=post_type
            form.content.data=post.content
            form.title.data=post.title


    return render_template('test.html',form=form)




