from flask import Blueprint, render_template

users=Blueprint('users', __name__)

@users.route("/login")
def login():
    return render_template("login.html", title="Login")

@users.route("/signup")
def signup():
    return render_template("signup.html", title="Signup")

@users.route('/account')
def home():
    return render_template('account.html', title="Account")