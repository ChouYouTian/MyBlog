from flask import render_template, url_for, redirect, request,flash,Blueprint
from flask_login import current_user,login_required
from .forms import PostForm,TestForm,UpdatePostForm,DeleteForm
from .util import saveimg_in_sever,get_post,update_post,post_draft,\
                    get_posts,add_post,test_add_post,delete_post


posts=Blueprint('posts',__name__)


#users posts and drafts
@posts.route('/post')
@login_required
def post():
    form=DeleteForm()
    my_posts=get_posts(current_user.id,'post')
    my_drafts=get_posts(current_user.id,'draft')

    
    return render_template('posts/mypost.html',form=form,posts=my_posts,drafts=my_drafts)

#get post by post id
@posts.route('/post_id')
def post_id():
    id=request.args.get('id')
    post=get_post(id,'post')

    return render_template('posts/post_id.html',post=post)

#create new post or draft
@posts.route('/post_new',methods=["POST", "GET"])
@login_required 
def post_new():

    form=PostForm()
    if form.validate_on_submit():
        success=False
        if form.post.data:
            print(form.tags.data)
            success= add_post(form.title.data,form.content.data,form.tags.data,'post')
            if success:
                flash('posted','success')

        elif form.save.data:
   
            success= add_post(form.title.data,form.content.data,form.tags.data,'draft')
            if success :
                flash('Draft saved','success')
 
        if not success:
            flash('Failed! Please try again', 'danger')
            return render_template('posts/editor.html',form=form,post_type='new')
        else:
            return redirect(url_for('posts.post'))

    elif request.method=="GET":
        return render_template('posts/editor.html',form=form,post_type='new')
    
   
    else:
        return render_template('errors/404.html'),404



#edit post or edit draft and post as post
@posts.route('/editor',methods=["POST", "GET"])
@login_required
def editor():
    id=request.args.get('id')
    post_type=request.args.get('type')

    try:
        post=get_post(id,post_type)
    except Exception as e:
        return render_template('errors/404.html'),404

    if post.author!=current_user:
        return render_template('errors/403.html'),403

    form=PostForm()
    if form.validate_on_submit():

        if form.save.data:
            success=update_post(post,title=form.title.data,content=form.content.data,tagstr=form.tags.data)
            if success:
                flash('Your post has been updated!', 'success')
                return redirect(url_for('main.home'))
            else:
                flash('Your post did\'t updated! Please try again', 'danger')
                return redirect(url_for('posts.post')),500
            
        elif form.post.data:
            success=post_draft(post,title=form.title.data,content=form.content.data)
            if success:
                flash('Your draft has been posted!', 'success')
                return redirect(url_for('main.home'))
            else:
                flash('Your draft did\'t posted! Please try again', 'danger')
                return redirect(url_for('posts.post')),500
        elif form.delete.data:
            success=delete_post(post)

            if success:
                if post_type=='post':
                    flash('Your post has been deleted!', 'success')
                elif post_type=='post':
                    flash('Your draft has been deleted!', 'success')

                return redirect(url_for('posts.post'))
            else:
                return render_template('errors/500.html'),500

    elif request.method=='GET':
        form.content.data=post.content
        form.title.data=post.title
        tagstr=''
        for tag in post.tag_rel:
            tagstr+='#'+tag.tag_type+' '
        form.tags.data=tagstr
        return render_template('posts/editor.html',form=form,post_type=post_type,id=id)

    elif request.method=="DELETE":
        print('delete')
    else:
        return render_template('errors/404.html'),404

@posts.route('/delete',methods=['POST'])
@login_required
def delete():
    id=request.args.get('id')
    post_type=request.args.get('type')
    
    try:
        post=get_post(id,post_type)
    except Exception as e:
        return render_template('errors/404.html'),404

    if post.author!=current_user:
        return render_template('errors/403.html'),403

    form=DeleteForm()
    if form.validate_on_submit():
        success=delete_post(post)

        if success:
            if post_type=='post':
                flash('Your post has been deleted!', 'success')
            elif post_type=='post':
                flash('Your draft has been deleted!', 'success')

            return redirect(url_for('posts.post'))
        else:
            return render_template('errors/500.html'),500
    else:
        return render_template('errors/404.html'),404


#saving img in sever and return path
@posts.route('/saveimg',methods=["POST"])
@login_required
def saveimg():
    if request.method=='POST':
        form_picture=request.files.get('image')
        return saveimg_in_sever(form_picture)

@posts.route('/search')
def search():
    tag=request.args.get('tag')
    if tag:
     
        posts=get_posts(tag)
        return render_template('posts/search.html',posts=posts)




@posts.route('/summer',methods=["POST","GET"])
def summer():
    if request.method=='POST':
        content=request.form.get('content')
        # print(content)
    return render_template('posts/summernote.html')



@posts.route('/test',methods=["Get","POST"])
@login_required 
def test():

    form=PostForm()
    if form.validate_on_submit():
        success=False
        if form.post.data:
            print(form.tags.data)
            success= test_add_post(form.title.data,form.content.data,form.tags.data,'post')
            if success:
                flash('posted','success')


        return render_template('posts/test.html',form=form)

    elif request.method=="GET":
        return render_template('posts/test.html',form=form,tags='apple,Apple,banana')
   
