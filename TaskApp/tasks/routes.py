from flask import Blueprint, render_template, url_for, redirect, flash, abort, request, jsonify, current_app
from TaskApp import db
from TaskApp.tasks.forms import TaskForm
from flask_login import login_required, current_user
from TaskApp.models import Task
from datetime import datetime
import secrets
from TaskApp.tasks.utils import send_task_notification,delete_expired_tasks

tasks=Blueprint('tasks', __name__)


# Task list route: Display all users tasks just title and small description not all and sort by due_date
@tasks.route("/tasks")
@login_required
def task_list():
    tasks = Task.query.filter_by(user_id=current_user.id)
    tasks=tasks.filter(Task.due_date > datetime.now() ).filter( Task.completed == False).order_by(Task.due_date.desc()).all()

    formatted_tasks = [{'title': task.title,
                        'due_date': task.due_date,
                        "task_secret":task.task_secret,
                        "importance": task.importance
                        } for task in tasks]
    return render_template("tasks.html", tasks=formatted_tasks, title="Task List")

# New route to get tasks for a specific view (e.g., "tasks", "expired", "completed")
@tasks.route("/tasks/<view>")
@login_required
def get_tasks_by_view(view):
    if view == "expired":
        # Delete expired tasks before fetching the tasks to display
        delete_expired_tasks()
        
    task = Task.query.filter_by(task_secret=view).first()
    if task:
        formatted_task = {'title': task.title,
                        'description': task.description,
                        'importance': task.importance,
                        'due_date': task.due_date.strftime('%Y-%m-%d %H:%M'),
                        "task_secret":task.task_secret 
                        }
        return render_template('task.html', task=formatted_task, title="Task")
    
    tasks_query = Task.query.filter_by(user_id=current_user.id)

    if view == "expired":
        tasks_query = tasks_query.filter(Task.due_date < datetime.now()).filter(Task.completed != True)
    elif view == "completed":
        tasks_query = tasks_query.filter(Task.completed == True)
    
    tasks = tasks_query.order_by(Task.due_date.desc()).all()

    formatted_tasks = [{'title': task.title,
                        'due_date': task.due_date,
                        'task_secret': task.task_secret,
                        'importance': task.importance
                        } for task in tasks]

    return render_template("tasks.html", tasks=formatted_tasks, title="Task List")

# Route to handle checkbox and completed tasks
@tasks.route("/tasks/complete/<task_secret>", methods=["POST"])
@login_required
def complete_task(task_secret):
    task = Task.query.filter_by(task_secret=task_secret, user_id=current_user.id).first_or_404()

    # Toggle the 'completed' field
    task.completed = not task.completed
    
    db.session.commit()
    
    return redirect(url_for('tasks.task_list'))

# Route to display the specific task and the information retated to it
@tasks.route('/tasks/<task_secret>')
@login_required
def task(task_secret):
    task = Task.query.filter_by(task_secret=task_secret).first()
    
    formatted_task = {'title': task.title,
                      'description': task.description,
                      'importance': task.importance,
                      'due_date': task.due_date.strftime('%Y-%m-%d %H:%M'),
                      "task_secret":task.task_secret 
                      }
    return render_template('task.html', task=formatted_task, title="Task")

#Route to create task and add it to the form then the database
@tasks.route("/tasks/create_task", methods=["GET","POST"])
@login_required
def create_task():
    secret=secrets.token_hex(20)
    form=TaskForm()
    if form.validate_on_submit():
        task=Task(title=form.title.data,
                  description=form.description.data,
                  due_date=form.due_date.data,
                  importance=form.importance.data,
                  user_id=current_user.id,
                  task_secret= secret,
                  completed=False
                  )
        db.session.add(task)
        db.session.commit()
        '''send_task_notification("Task Created",
                                f"Your task {form.title.data} has been created.",
                                form.title.data,
                                    secret)'''
        return redirect(url_for("tasks.task_list")) 
    return render_template("create_task.html", title="New Task", legend="New Task", form=form)

#Route to update tasks
@tasks.route("/task/<task_secret>/update_task", methods=["GET","POST"])
@login_required
def update_task(task_secret):
    task=Task.query.filter_by(task_secret=task_secret).first_or_404()
    if task.user_id != current_user.id:
        abort(403)
    form=TaskForm()
    if form.validate_on_submit():
        task.title=form.title.data
        task.description=form.description.data
        task.due_date= form.due_date.data
        task.importance=form.importance.data
        db.session.add(task)
        db.session.commit()
        flash('Your Task Has Been Updated', 'success')
        return redirect(url_for("tasks.task_list", user_id=current_user.id))
    elif request.method == 'GET':
        form.title.data=task.title
        form.due_date.data=task.due_date
        form.description.data=task.description
        form.importance.data=task.importance

    return render_template("create_task.html", title="Update Task", legend="New Task", form=form)

# Route to handle function to delete task
@tasks.route("/task/<task_secret>/delete")
@login_required
def delete_task(task_secret):
    task=Task.query.filter_by(task_secret=task_secret).first_or_404()
    if task.user_id != current_user.id:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Your Task Has Been Deleted', 'success')
    return redirect(url_for("tasks.task_list"))


