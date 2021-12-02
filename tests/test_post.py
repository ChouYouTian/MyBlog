from operator import sub
import os

import flask_login
path=os.getcwd()
import sys
sys.path.append(path)

import unittest
from myweb import create_app,db,bcrypt
from flask_testing import TestCase
from flask import url_for
from myweb.models import User,Post,Draft
from flask_login import current_user,login_user,logout_user




class SettingBase(TestCase):
    def create_app(self):
        return create_app('testing')
    
    counter=1
    
    # 在運行測試之前會先被執行
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.add_user()


    # 在結束測試時會被執行
    def tearDown(self):
        logout_user()
        db.session.remove()
        db.drop_all()

    def add_user(self):
        hashedPassword=bcrypt.generate_password_hash('admin').decode('utf-8')
        user=User(username='admin',email='admin@g.c',password=hashedPassword)
        db.session.add(user)
        
        hashedPassword=bcrypt.generate_password_hash('test').decode('utf-8')
        test=User(username='test',email='test@g.c',password=hashedPassword)
        db.session.add(test)
        
        db.session.commit()

        self.admin=user
        self.test=test

    def add_post(self,title,content):
        post=Post(title=title,content=content,author=current_user)

    
    def login(self,name='admin',password='admin'):
        response=self.client.post(url_for('users.login'),
                                    follow_redirects=True,
                                    data={
                                        "email_name": name,
                                        "password":password,
                                        "submit":True
                                    })
        return response
    def post(self,title='title',content='content',submit=True,save=False):
        if submit==True:
            response=self.client.post(url_for('posts.post_new'),
                                        follow_redirects=True,
                                        data={
                                            "title": title,
                                            "content":content,
                                            "submit":submit
                                        })
        elif save:
            response=self.client.post(url_for('posts.post_new'),
                                    follow_redirects=True,
                                    data={
                                        "title": title,
                                        "content":content,
                                        "save_draft":save
                                    })
        return response

        

class CheckUserAndLogin(SettingBase):
    # def test_signup(self):
    #     response = self.signup()
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.request.path,url_for('users.login'))

    def test_post(self):
        with self.client:
            self.login()
            response=self.post()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.request.path,url_for('posts.post'))
            self.assertIn(b'posted',response.data)

    def test_draft(self):
        print('test draft')
        with self.client:
            self.login()
            response=self.post(submit=False,save=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.request.path,url_for('posts.post'))
            # self.assertIn(b'posted',response.data)
            self.assertIn(b'Draft saved',response.data)

if __name__=='__main__':
    unittest.main()