from flask_mail import Message
from TaskApp import apscheduler, mail
from flask_login import current_user
from flask import url_for
from datetime import datetime, timedelta
from TaskApp.models import Task, User
from TaskApp import db

def delete_expired_tasks():
    expiration_limit = datetime.now() - timedelta(hours=1)
    expired_tasks = Task.query.filter(Task.due_date < expiration_limit).filter(Task.completed != True).all()

    for task in expired_tasks:
        db.session.delete(task)
    
    db.session.commit()

def send_task_notification(subject, body,task_title, task_secret,):
    msg = Message(subject=subject,sender= "noreply@demo.com", recipients=[current_user.email])
    task_url = url_for('tasks.task', task_secret=task_secret, _external=True)

    # Add a link to the task details page in the email body
    msg.html = f"{body}<br><a href='{task_url}'>{task_title}</a>"

    msg.body = body
    mail.send(msg)

def send_task_reminder( mail, task):
    user = User.query.get(task.user_id)

    # Check if the user exists and has an email
    if user and user.email:
        subject = "Task Expiration Reminder"
        body = f"Reminder: Your task '{task.title}' is about to expire in 1 hour. Ensure you complete it and check complete :) "

        msg = Message(subject=subject,sender= "noreply@demo.com", recipients=[user.email])
        msg.body = body

        # Add a link to the task details page in the email body
        msg.html = f"{body}<br>"

        mail.send(msg)
        

# Schedule the task reminder job
def task_reminder():
    with apscheduler.app.app_context():
        # Get tasks that are about to expire in 1 hour
        expiration_limit = datetime.now() + timedelta(hours=1)
        tasks_to_remind = Task.query.filter(Task.due_date.between(datetime.now(), expiration_limit)).all()

        # Send reminder for each task
        for task in tasks_to_remind:
            send_task_reminder(mail, task)


apscheduler.add_job(
    func=task_reminder,  
    trigger='interval',  
    hours=1,  
    id='task_reminder'  
)