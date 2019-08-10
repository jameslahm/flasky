from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Email,DataRequired,Length,EqualTo,Regexp
from wtforms import ValidationError
from ..models import User,Role

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Length(1,64),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember_me=BooleanField('Keep me logged in')
    submit=SubmitField('Log in')

class RegisterForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Length(1,64),Email()])
    username=StringField('Username',validators=[DataRequired(),Length(1,64),Regexp("^[A-Za-z][A-Za-z_1-9.]*$",0,'Usernames must have letters,numbers,dots or underscores')])
    password=PasswordField('Password',validators=[DataRequired(),EqualTo('password2',message="Passwords must match")])
    password2=PasswordField('Confirm Password',validators=[DataRequired()])
    submit=SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered")
        
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already in use")

class ChangePasswordForm(FlaskForm):
    old_password=PasswordField("Old password",validators=[DataRequired()])
    password=PasswordField("New password",validators=[DataRequired(),EqualTo('password2',message="Password must match")])
    password2=PasswordField("Confirm new password",validators=[DataRequired()])
    submit=SubmitField("Update Password")

class PasswordReserRequestForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Length(1,64),Email()])
    submit=SubmitField("Reset Password")

class ChangeEmailForm(FlaskForm):
    email=StringField("New Email",validators=[DataRequired(),Length(1,64),Email()])
    password=PasswordField("Password",validators=[DataRequired()])
    submit=SubmitField('Update Email Address')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("Email already registered")

class PasswordResetForm(FlaskForm):
    password=PasswordField('New Password',validators=[DataRequired(),Length(1,64),EqualTo('password2',message="Password must match")])
    password2=PasswordField("Confirm Your Password",validators=[DataRequired(),Length(1,64)])
    submit=SubmitField('Reset Password')