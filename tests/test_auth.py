import os
path=os.getcwd()
import sys
sys.path.append(path)

import unittest
from myweb import create_app,db,bcrypt
from flask_testing import TestCase
from flask import url_for
from myweb.models import User




class SettingBase(TestCase):
    def create_app(self):
        return create_app('testing')
    
    # 在運行測試之前會先被執行
    def setUp(self):
        db.create_all()

        hashedPassword=bcrypt.generate_password_hash('admin').decode('utf-8')
        user=User(username='admin',email='admin@g.c',password=hashedPassword)

        db.session.add(user)
        db.session.commit()

        self.username = "test"
        self.email="test@g.c"
        self.password = "test"
        self.confirmPassword="test"

    # 在結束測試時會被執行
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # signup 是測試時很常會被用到的功能，所以寫成函式，可以重複利用
    def signup(self):
        response = self.client.post(url_for('users.signup'),
                                    follow_redirects=True,
                                    data={
                                        "username": self.username,
                                        "email":self.email,
                                        "password": self.password,
                                        "confirmPassword":self.confirmPassword,
                                        "submit":True
                                    })
        return response
    
    def login(self):
        response = self.client.post(url_for('users.login'),
                                    follow_redirects=True,
                                    data={
                                        "email_name": 'admin',
                                        "password":"admin",
                                        "submit":True
                                    })
        

class CheckUserAndLogin(SettingBase):
    def test_signup(self):
        response = self.signup()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path,url_for('users.login'))

    def test_signup_confirmpsw_wrong(self):
        self.confirmPassword="testttt"
        response = self.signup()
        # print(response.status_code)
        self.assert400(response)
        self.assertEqual(response.request.path,url_for('users.signup'))
        self.assertIn(b'Field must be equal to password.',response.data)

    def test_signup_psw_wrong(self):
        self.password="testttt"
        response = self.signup()
        self.assert400(response)
        self.assertEqual(response.request.path,url_for('users.signup'))
        self.assertIn(b'Field must be equal to password.',response.data)

    def test_signup_email_wrongsyntax(self):
        self.email='test@'
        response = self.signup()
        self.assert400(response)
        self.assertEqual(response.request.path,url_for('users.signup'))
        self.assertIn(b'Invalid email address.',response.data)

    def test_signup_dubblesingup(self):

        self.signup()
        response = self.signup()

        self.assert400(response)
        self.assertEqual(response.request.path,url_for('users.signup'))
        self.assertIn(b'This email has been taken.Please Check again.',response.data)
        
        

    # def test_login(self):
    #     self.login()

    #     response = self.client.post(url_for('users.login'),
    #                                 follow_redirects=True,
    #                                 data={
    #                                     "email_name": 'admin',
    #                                     "password":"admin",
    #                                     "submit":True
    #                                 })
    #     print(response.status_code)



    # def test_signup_400(self):
    #     # 測試密碼少於六位數
    #     self.passwords = '123'
    #     self.confirmPassword="123"
    #     response = self.signup()
    #     self.assertEqual(response.status_code, 200)


if __name__=='__main__':
    unittest.main()