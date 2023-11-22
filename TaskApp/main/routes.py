from flask import Blueprint, render_template
from flask_login import current_user

main=Blueprint('main', __name__)

#Home route
@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', title="TaskGenius")