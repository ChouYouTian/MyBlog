from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import mysql
import pymysql
from .config.Config import config


db = SQLAlchemy()
bcrypt = Bcrypt()
loginManager=LoginManager()
loginManager.login_view='users.login'
loginManager.login_message_category='info'



def create_app(config_name):
    app = Flask(__name__,template_folder="templates")
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    bcrypt.init_app(app)
    loginManager.init_app(app)


    from myweb.users.routes import users
    from myweb.posts.routes import posts
    from myweb.main.routes import main
    from myweb.errors.handler import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app