from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,EqualTo,Email,ValidationError
from flask_wtf.file import FileField,FileAllowed
from myweb.models import User
from flask_login import current_user



class SignUpForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=3,max=10)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=3,max=10)])
    confirmPassword=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])


    submit=SubmitField('SignUp')

    def validate_email(self,email):
        validated=User.query.filter_by(email=email.data).first()

        if validated:
            raise ValidationError('This email has been taken.Please Check again.')
        


class LoginForm(FlaskForm):
    email_name=StringField('Email or Name',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=3,max=10)])
    remeber=BooleanField('Remeber Me')
    
    submit=SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=3,max=10)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    picture=FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])

    submit=SubmitField('SignUp')

    def validate_email(self,email):
        
        if email.data != current_user.email:
            validated=User.query.filter_by(email=email.data).first()
            if validated:
                raise ValidationError('This email has been taken.Please Check again.')
            
