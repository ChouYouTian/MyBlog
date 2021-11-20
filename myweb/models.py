from myweb import db,loginManerger
from datetime import datetime
from flask_login import UserMixin



@loginManerger.user_loader
def load_user(userID):
    return User.query.get(int(userID))

tag_relations=db.Table(
    'tag_relations',
    db.Column('tag_rel',db.Integer,db.ForeignKey('tag.id')),
    db.Column('post_rel',db.Integer,db.ForeignKey('post.id'))
)


class User(db.Model,UserMixin):

    id=db.Column(db.Integer,primary_key=True)

    username=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(120),nullable=False,unique=True)
    password=db.Column(db.String(60),nullable=False)

    date_joined=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    image_file=db.Column(db.String(20),nullable=False,default='default.png')


    posts = db.relationship('Post', backref='author', lazy=True)
    drafts = db.relationship('Draft', backref='author', lazy=True)

    
    def __repr__(self) -> str:
        return f'User(id {self.id},name {self.username})'


class Post(db.Model):

    id=db.Column(db.Integer,primary_key=True)

    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)

    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    date_updated=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    tags=db.relationship('Tag',secondary=tag_relations,backref='post')

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Draft(db.Model):

    id=db.Column(db.Integer,primary_key=True)

    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)

    date_saved=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    date_updated=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Draft('{self.title}', '{self.date_posted}')"

class Tag(db.Model):

    id=db.Column(db.Integer,primary_key=True)

    tag_type=db.Column(db.String(20),nullable=False)

    date_saved=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    date_updated=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"tag('{self.id}', '{self.date_saved}')"

        