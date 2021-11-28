from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,SubmitField,TextAreaField,IntegerField
from wtforms.validators import DataRequired



class PostForm(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    content=TextAreaField('Content',validators=[DataRequired()])

    submit=SubmitField('Post')
    save_draft=SubmitField('Save')

class UpdatePostForm(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    content=TextAreaField('Content',validators=[DataRequired()])
    save=SubmitField('Save',default=False)
    post=SubmitField('Post',default=False)

class TestForm(FlaskForm):
    picture=FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('send img')

