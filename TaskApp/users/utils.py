from flask import url_for
from flask_mail import Message
from TaskApp import mail


#Send email after forgotten password is clicked
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(subject='Password Request Reset',
                sender='noreply@demo.com',
                recipients=[user.email]
                )
    msg.body=f'''To reset your password, visit the following link:
    
    {url_for('users.reset_token', token=token, _external=True)}

    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)

