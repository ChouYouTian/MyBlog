from typing import overload
from PIL import Image
import os
import secrets
from myweb import db
from myweb.models import Post,Draft ,Tag,post_tag_relations
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


@overload
def get_posts(id:int,post_type:str):
    '''
    input: post_type=Post or Draft , id = user id
    return: posts or none
    get posts filter by id and type of post(ex.post draft)
    '''

@overload
def get_posts(tag:str):
    '''
    input: tag
    return: posts or none
    get posts filter by tag
    '''

def get_posts(*args,**kargs):

    if isinstance(args[0],int):
        id=args[0]
        post_type=args[1]
        tag=None
    elif isinstance(args[0],str):
        id=None
        post_type=None
        tag=args[0]
    else:
        id=kargs.get('id')
        post_type=kargs.get('post_type')
        tag=kargs.get('tag')
    
    if isinstance(id,int) and isinstance(post_type,str):
        if post_type=='post':
            posts=Post.query.filter_by(user_id=id)
        elif post_type=='draft':
            posts=Draft.query.filter_by(user_id=id)
        else:
            return None
    
        return posts
    elif isinstance(tag,str):
        
        tid=get_tag_id(tag)
        if tag:
          
            pids=[tag.post_rel for tag in db.session.query(post_tag_relations).filter_by(tag_rel=tid).all()]
            posts=Post.query.filter(Post.id.in_(pids)).all()

            for p in posts:
                print(p)
            return posts
        else:
            return None

    return None





def update_post(post,title:str,content:str,tagstr:str):
    """
    select post by id and post_type and update with new title or content 
    """
    taglist=get_tags(tagstr)
    try:
        post.title=title
        post.content=content
        post.tag_rel=taglist
        post.date_updated=datetime.utcnow()
        db.session.commit()
    except:
        db.session.rollback()
        return False
    else:
        return True


def post_draft(post,title,content):
    content=post.content
    title=post.title
    tag_rel=post.tag_rel
    try:
        newpost=Post(title=title,content=content,author=current_user,tag_rel=tag_rel)
        db.session.add(newpost)
        db.session.delete(post)
        db.session.commit()
    except:
        db.session.rollback()
        return False
    else:
        return True




def add_post(title,content,tagstr,type:str):
    taglist=get_tags(tagstr)
    try:
        if type=='post':
            add_post= Post(title=title,content=content,author=current_user,tag_rel=taglist)
        elif type=='draft':
            add_post= Draft(title=title,content=content,author=current_user,tag_rel=taglist)

        db.session.add(add_post)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False

    return True

def delete_post(post:Post):
    try:
        db.session.delete(post)
        db.session.commit()
    except:
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


def create_tag(tag_type):
    tag=Tag(tag_type=tag_type)
    db.session.add(tag)
    db.session.commit()
        
    return tag

def get_tag_id(tag_type):
    tag=Tag.query.filter_by(tag_type=tag_type).first()
    return tag.id

def get_taglist(tagstr:str):
    taglist=[]
    index=0
    print(tagstr)
    while True:
        tagStart=tagstr.find('#',index)
        tagEnd=tagstr.find(' ',index)
        if tagStart==-1:
            break
        if tagEnd==-1:
            taglist.append(tagstr[tagStart+1:])
            break
        else:
            taglist.append(tagstr[tagStart+1:tagEnd])
            index=tagEnd+1
    print(taglist)
    return taglist


def get_tags(tagstr:str):
    taglist=get_taglist(tagstr=tagstr)
    rlist=[]
    for tag_type in taglist:
        tag=Tag.query.filter_by(tag_type=tag_type).first()
        if tag:
            rlist.append(tag)
        else:
            newtag=create_tag(tag_type)
            rlist.append(newtag)
    
    return rlist
    


def test_add_post(title,content,tagstr,type:str):
    taglist=get_tags(tagstr)

    try:
        if type=='post':
            add_post= Post(title=title,content=content,author=current_user,tag_rel=taglist)
        elif type=='draft':
            add_post= Draft(title=title,content=content,author=current_user)

        db.session.add(add_post)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False
    # for tag in add_post.tag_rel:
        # print(tag.tag_type)
    return True