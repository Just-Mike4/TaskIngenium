from flask_mail import Message
from TaskApp import mail
from flask_login import current_user
from flask import url_for


def send_task_notification(subject, body,task_title, task_secret,):
    msg = Message(subject=subject,sender= "noreply@demo.com", recipients=[current_user.email])
    task_url = url_for('tasks.task', task_secret=task_secret, _external=True)

    # Add a link to the task details page in the email body
    msg.html = f"{body}<br><a href='{task_url}'>{task_title}</a>"

    msg.body = body
    mail.send(msg)

