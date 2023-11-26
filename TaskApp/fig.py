import os
#Config class that will be called to create the application with the following configurations
class Config():
    SECRET_KEY = 'bda6feb17068a6d336e073324979f281'
    SQLALCHEMY_DATABASE_URI ='sqlite:///Task.db' 
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get('TASKGENNAME')
    MAIL_PASSWORD = os.environ.get('TASKGENPASS')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
