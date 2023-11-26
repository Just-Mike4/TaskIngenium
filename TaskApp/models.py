from datetime import datetime
from TaskApp import db, login_manager
from flask_login import UserMixin
from flask import current_app
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import jwt

#Allows flask-login manager to know information about the logged-in user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#The user model and needed columns 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    tasks = db.relationship('Task', backref='author', lazy=True)

    #Function that gets the reset token in a random hex format and sets expriing time
    def get_reset_token(self, expires_sec=1800):
        reset_token = jwt.encode(
            {
                "confirm": self.id,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                       + datetime.timedelta(seconds=expires_sec)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return reset_token
    
    #To verify the reset token sent and used to change user password
    @staticmethod
    def verify_reset_token(token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = data.get('confirm')  # Use the key you specified in get_reset_token
            return User.query.get(user_id)
        except ExpiredSignatureError:  
            return None
        except InvalidTokenError:
            return None

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

#The Task Model and needed columns
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    due_date=db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    importance=db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_secret=db.Column(db.String(20), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, title, due_date, importance, task_secret, completed, user_id, description):
        self.title = title
        self.due_date = due_date
        self.importance = importance
        self.task_secret = task_secret
        self.completed = completed
        self.user_id = user_id
        self.description=description

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"