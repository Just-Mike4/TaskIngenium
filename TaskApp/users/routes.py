from flask import Blueprint, render_template

users=Blueprint('users', __name__)


@users.route('/account')
def home():
    return render_template('home.html')