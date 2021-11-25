from PIL import Image
import os
import secrets
from myweb import db
from myweb.models import Post,Draft 
from flask_login import current_user
from flask import current_app
from datetime import datetime



def get_post(id,post_type):
    '''
    input: post_type=Post or Draft , id = for id in db
    return: post or none
    get post by id and type of post(ex.post draft)
    '''
    if post_type=='post':
        post=Post.query.get(id)
    elif post_type=='draft':
        post=Draft.query.get(id)
    else:
        return None
 
    return post

def get_posts(id,post_type):
    '''
    input: post_type=Post or Draft , id = for id in db
    return: posts or none
    get posts filter by id and type of post(ex.post draft)
    '''
    if post_type=='post':
        posts=Post.query.filter_by(user_id=id)
    elif post_type=='draft':
        posts=Draft.query.filter_by(user_id=id)
    else:
        return None
 
    return posts

def update_post(post,title,content):

    post.title=title
    post.content=content
    post.date_updated=datetime.utcnow()
    db.session.commit()
    return

def update_post(id,post_type,title,content):
    if post_type=='post':
        post=Post.query.get(id)
    elif post_type=='draft':
        post=Draft.query.get(id)
        
    post.title=title
    post.content=content
    post.date_updated=datetime.utcnow()
    db.session.commit()
    return


def post_draft(post,title,content):
    newpost=Post(title=title,content=content,author=current_user)
    db.session.add(newpost)
    db.session.delete(post)
    db.session.commit()




def add_posts(title,content,type):
    if type=='post':
        add_post= Post(title=title,content=content,author=current_user)
    elif type=='draft':
        add_post= Draft(title=title,content=content,author=current_user)

    db.session.add(add_post)
    db.session.commit()

    return True



def saveimg_in_sever(img)->str:
    '''
    input: img file
    return: img path in sever
    '''
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(img.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/picture/temp', picture_fn)

    i = Image.open(img)
    i.save(picture_path)

    return 'static/picture/temp/'+picture_fn