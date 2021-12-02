import os
path=os.getcwd()
import sys
sys.path.append(path)

from myweb import db,bcrypt,create_app
from myweb.models import User,Tag,Post,post_tag_relations
app=create_app('development')


if __name__=="__main__":
    with app.app_context():
        # tags=db.session.query(post_tag_relations).filter_by(tag_rel=1).all()
        
        posts=Post.query.filter(Post.tag_rel.any(tag_type='python')).all()
        print(posts)
        
        # for q in posts:
        #     print(q)

            

     