from flask_wtf import Form
from wtforms import StringField,PasswordField,TextAreaField,DateField,SelectField,RadioField,BooleanField
from wtforms.validators import (DataRequired, Regexp, ValidationError,
                                Email, Length, EqualTo)
from models.models import Base,User,Product,ProductItem,DATABASE
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists
from flask.ext.bcrypt import generate_password_hash

engine = DATABASE
Base.metadata.bind = (engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

 
#Check if username exists
def name_exists(form, field):
    if session.query(exists().where(User.username == field.data)).scalar()  :
        raise ValidationError('User with the username already exists !')

#Check if email exists    
def email_exists(form, field):
    if session.query(exists().where(User.email == field.data)).scalar() :
        raise ValidationError('User with the email already exists !')

def pwd_thesame(form,field):
    if session.query(exists().where(User.email == field.data, User.password == generate_password_hash(field.data))).scalar() :
        raise ValidationError('Please select a different password !')


class RegisterForm(Form):
    username = StringField('Username',
                           validators = [DataRequired(),
                                         Regexp(r'^[a-zA-Z0-9_]+$',
                                         message = ("Username should be one word , letters,"
                                                    "numbers, and underscore only")),
                                         name_exists])
    email =  StringField('Email',validators = [DataRequired(),Email(),email_exists])
    password = PasswordField('Password',validators = [DataRequired(),Length(min=8),
                                        EqualTo('password2', message = 'Password does not match !')])
    password2 = PasswordField('Re-Enter Password')

class EditAccountForm(Form):
    title = RadioField('Title', choices =[('Mr','Male'),('Ms','Female')])
    fname = StringField('First Name')
    lname = StringField( 'Last Name')
    username = StringField('Username')
    email =  StringField('Email')
    password = PasswordField('Password')
    newpassword = PasswordField('New Password' ,validators = [DataRequired(),EqualTo('password2', message = 'Password does not match !')])
    password2 = PasswordField('Re-Enter Password')
    address = TextAreaField('Address')
    state = SelectField('State', choices=[('us','USA'),('gb','Great Britain'),('ru','Russia')])
                
                
class LoginForm(Form):
    email = StringField('Enter email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Password')