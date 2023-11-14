from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from TaskApp.fig import Config

mail=Mail()
db = SQLAlchemy()
bcrypt=Bcrypt()
login_manager=LoginManager()
login_manager.login_view='users.login'
login_manager.login_message_category='info'

mail=Mail()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from TaskApp.users.routes import users
    from TaskApp.tasks.routes import tasks
    from TaskApp.main.routes import main
    from TaskApp.errors.handlers import errors

    db.init_app(app)
    bcrypt.init_app(app)
    '''login_manager.init_app(app)'''
    mail.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(tasks)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    
    return app