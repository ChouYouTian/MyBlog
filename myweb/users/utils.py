import secrets
import os
from PIL import Image
from myweb import db,bcrypt
from myweb.models import User
from flask import current_app
from flask_login import current_user


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/picture', picture_fn)
    
    # resize the picture
    output_size = (125, 125)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def get_user_by_id_Email(email_name):
    user=User.query.filter_by(username=email_name).first()
    if not user:
        user=User.query.filter_by(email=email_name).first()
    
    return user


def update_account(username=None,email=None,imgData=None):
    if imgData:
        picturefile=save_picture(imgData)
        current_user.image_file=picturefile

    current_user.username=username
    current_user.email=email

    db.session.commit()

    return True

def sign_up_user(username,email,password):
    hashedPassword=bcrypt.generate_password_hash(password).decode('utf-8')
    user=User(username=username,email=email,password=hashedPassword)

    db.session.add(user)
    db.session.commit()

    return True

def check_user(email_name,password):
    user=get_user_by_id_Email(email_name)

    if user and bcrypt.check_password_hash(user.password,password):
        return user
    else:
        return False
