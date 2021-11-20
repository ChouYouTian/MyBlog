import os
path=os.getcwd()

import sys
sys.path.append(path)

from myweb import db,bcrypt
from myweb.models import User

if __name__=="__main__":
    hashedPassword=bcrypt.generate_password_hash('admin').decode('utf-8')
    user=User(username='admin',email='admin@g.c',password=hashedPassword)
    db.drop_all()
    db.create_all()

    db.session.add(user)
    db.session.commit()

    print(User.query.get(1))
