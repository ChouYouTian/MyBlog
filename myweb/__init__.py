from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import mysql
import pymysql
app = Flask(__name__,template_folder="templates")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "#230dec61-fee8-4ef2-a791-36f9e680c9fc"


# using sqlite for testing
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"


#using google cloud platform mysql
from mysqlconfig import *

# pymysql.install_as_MySQLdb()

# app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
# app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}:3306/{DBNAME}/{PROJECT_ID}:{INSTANCE_NAME}"
# app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}:3306/{DBNAME}"


db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
loginManerger=LoginManager(app)
loginManerger.login_view='login'
loginManerger.login_message_category='info'


from myweb import routes

