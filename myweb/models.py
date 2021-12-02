from myweb import db,loginManager
from datetime import datetime
from flask_login import UserMixin

@loginManager.user_loader
def load_user(userID):
    return User.query.get(int(userID))

post_tag_relations=db.Table(
    'post_tag_relations',
    db.Column('tag_rel',db.Integer,db.ForeignKey('tag.id')),
    db.Column('post_rel',db.Integer,db.ForeignKey('post.id'))
)

draft_tag_relations=db.Table(
    'draft_tag_relations',
    db.Column('tag_rel',db.Integer,db.ForeignKey('tag.id')),
    db.Column('draft_rel',db.Integer,db.ForeignKey('draft.id'))
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

    tag_rel = db.relationship(
        "Tag", secondary=post_tag_relations, backref="post")

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Draft(db.Model):

    id=db.Column(db.Integer,primary_key=True)

    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)

    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    date_updated=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    tag_rel = db.relationship(
        "Tag", secondary=draft_tag_relations, backref="draft")

    def __repr__(self):
        return f"Draft('{self.title}', '{self.date_posted}')"

class Tag(db.Model):

    id=db.Column(db.Integer,primary_key=True)

    tag_type=db.Column(db.String(20),nullable=False,unique=True)

    def __repr__(self) -> str:
        return f"tag('{self.id}')"

        