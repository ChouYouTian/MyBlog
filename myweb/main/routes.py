from flask import Blueprint,render_template
from myweb.models import Post

main=Blueprint('main',__name__)






@main.route('/')
@main.route('/home')
def home():
    posts=Post.query.all()
    return render_template('index.html', posts=posts)
