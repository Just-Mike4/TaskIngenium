from flask import Blueprint, render_template
from flask_login import current_user

main = Blueprint('main', __name__)

# Home route
@main.route('/')
@main.route('/home')
def home():
    # Display welcome (username) if user is logged in
    if current_user.is_authenticated:
        username = current_user.username
        return render_template('home.html', title="TaskIngenium", username=username)
    else:
        return render_template('home.html', title="TaskIngenium")

