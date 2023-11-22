from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from TaskApp.models import User

#The user signup form
class RegistrationForm(FlaskForm):
    username= StringField('Username',
                          validators=[DataRequired(),
                                      Length(min=2,max=20) ])
    email= StringField('Email',
                       validators=[DataRequired(),
                                  Email() ])
    password= PasswordField('Password',validators=[DataRequired()])

    confirm_password= PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                  EqualTo('password')])
    
    submit= SubmitField('Sign Up')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That Username is Taken. Please choose a different one")
        
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That Email is Taken. Please choose a different one")

#The user login form 
class LoginForm(FlaskForm):
    email= StringField('Email',
                       validators=[DataRequired(),
                                  Email() ])
    password= PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    
    submit= SubmitField('Login')


#User account form
class UpdateAccountForm(FlaskForm):
    username= StringField('Username',
                          validators=[DataRequired(),
                                      Length(min=2,max=20) ])
    email= StringField('Email',
                       validators=[DataRequired(),
                                  Email() ])
    
    
    submit= SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
             raise ValidationError("That Username is Taken. Please choose a different one")
        
    def validate_email(self,email):
        if email.data != current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("That Email is Taken. Please choose a different one")

#User reset request form
class RequestResetForm(FlaskForm):
    email= StringField('Email',
                       validators=[DataRequired(),
                                  Email() ])
    submit=SubmitField('Request Password Reset')
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email. You must register first")

#User reset password form
class ResetPasswordForm(FlaskForm):
    password= PasswordField('Password',validators=[DataRequired()])

    confirm_password= PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                  EqualTo('password')])
    submit=SubmitField('Reset Password')