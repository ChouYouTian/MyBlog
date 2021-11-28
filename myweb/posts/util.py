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
        post=Post.query.get_or_404(id)
    elif post_type=='draft':
        post=Draft.query.get_or_404(id)

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


def update_post(post,title:str,content:str):
    """
    select post by id and post_type and update with new title or content 
    """
    try:
        post.title=title
        post.content=content
        post.date_updated=datetime.utcnow()
        db.session.commit()
    except:
        db.session.rollback()
        return False
    else:
        return True


def post_draft(post,title,content):
    try:
        newpost=Post(title=title,content=content,author=current_user)
        db.session.add(newpost)
        db.session.delete(post)
        db.session.commit()
    except:
        db.session.rollback()
        return False
    else:
        return True




def add_post(title,content,type:str):
    try:
        if type=='post':
            add_post= Post(title=title,content=content,author=current_user)
        elif type=='draft':
            add_post= Draft(title=title,content=content,author=current_user)

        db.session.add(add_post)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False

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