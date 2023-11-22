from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from TaskApp import db, bcrypt
from TaskApp.models import User
from TaskApp.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from TaskApp.users.utils import send_reset_email
from sqlalchemy import text

users=Blueprint('users', __name__)

#The user signup route
@users.route("/signup", methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your Account has been Created! You are now able to  Login ', 'success')
        return redirect(url_for('users.login'))
    return render_template('signup.html', title='Register',form=form)

#The user login route
@users.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=LoginForm()
    if form.validate_on_submit():
       user=User.query.filter_by(email=form.email.data).first()
       if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember= form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else  redirect(url_for('main.home'))
       else:
        flash("Login Unsuccessful. Please Check Username And Password","danger")
    return render_template('login.html', title='Login',form=form)

#The user logout route
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

#The user account route
@users.route("/account", methods=['GET','POST'])
@login_required
def account():
     form=UpdateAccountForm()
     if form.validate_on_submit():

         current_user.username= form.username.data
         current_user.email = form.email.data
         db.session.commit()
         flash('Your Account Has Been Updated!', 'success')
         return redirect(url_for('user.account'))
     
     elif request.method== 'GET':
         form.username.data= current_user.username
         form.email.data = current_user.email
        
     return render_template('account.html', title='Account',
                              form=form)

#The user reset passowrd route
@users.route("/reset_password",methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("Your Email has been sent with instructions to reset your password", 'info')
        return redirect(url_for('user.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

#The secret reset password route
@users.route("/reset_password/<token>",methods=['GET','POST'])
def reset_token(token):
     if current_user.is_authenticated:
        return redirect(url_for('main.home'))
     user= User.verify_reset_token(token)
     if user is None:
         flash('That is an Invalid or Expired Token', 'warning')
         return redirect(url_for('user.reset_request'))
     form= ResetPasswordForm()
     if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_password
        db.session.commit()
        flash('Your Password has been updated! You are now able to  Login ', 'success')
        return redirect(url_for('user.login'))
     return render_template('reset_token.html', title='Reset Password', form=form)

#Delete user account route     
@users.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    if request.method == 'POST':
        user = current_user

        db.session.delete(user)
        db.session.commit()
        with db.engine.connect() as connection:
            connection.execute(text("VACUUM"))
        
        db.session.commit()
        

        flash('Your account has been deleted.', 'success')
        return redirect(url_for('users.logout'))

 
    return redirect(url_for('main.home'))