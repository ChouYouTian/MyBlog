import os
path=os.getcwd()

import sys
sys.path.append(path)

from myweb import db,bcrypt,create_app
from myweb.models import User
app=create_app('development')

if __name__=="__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()

        users=[]

        hashedPassword=bcrypt.generate_password_hash('admin').decode('utf-8')
        user=User(username='admin',email='admin@g.c',password=hashedPassword)
        users.append(user)
        for i in range(1,2):
            hashedPassword=bcrypt.generate_password_hash(f'test{i}').decode('utf-8')
            user=User(username=f'test{i}',email=f'test{i}@g.c',password=hashedPassword)
            users.append(user)

        db.session.add_all(users)
        db.session.commit()

        print(User.query.get(1))
