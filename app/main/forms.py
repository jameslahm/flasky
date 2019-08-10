from flask_wtf import FlaskForm
from wtforms import SelectField,BooleanField,TextAreaField,StringField, SubmitField
from wtforms.validators import DataRequired,Length,Email,Regexp,ValidationError
from flask_sqlalchemy import SQLAlchemy
from ..models import User,Role
from flask_pagedown.fields import PageDownField

class NameForm(FlaskForm):
    name = StringField("what is your name", validators=[DataRequired()])
    submit = SubmitField("submit")

class EditProfileForm(FlaskForm):
    name=StringField("Real name",validators=[Length(0,64)])
    location=StringField("Location",validators=[Length(0,64)])
    about_me=TextAreaField("About_me")
    submit=SubmitField('Submit')

class EditProfileAdminForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Length(1,64),Email()])
    username=StringField("username",validators=[DataRequired(),Length(1,64),Regexp("^[A-Za-z][A-Za-z0-9_.]*$",0,'Username must have only letters,numbers,dots,or underscores')])
    confirmed=BooleanField('Confirmed')
    role=SelectField("Role",corece=int)
    name=StringField('Real name',validators=[Length(0,64)])
    location=StringField("Location",validators=[Length(0,64)])
    about_me=TextAreaField("About me")
    submit=SubmitField('Submit')

    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices=[(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
        self.user=user
    
    def validate_email(self,field):
        if self.user.email!=field.data and User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered")

    def validate_username(self,field):
        if self.user.username!=field.data and User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already in use")
    
class PostForm(FlaskForm):
    body=PageDownField("What's on your mind?",validators=[DataRequired()])
    submit=SubmitField('Submit')

class CommentForm(FlaskForm):
    body=StringField('',validators=[DataRequired()])
    submit=SubmitField('Submit')

