from flask import Blueprint, render_template, url_for, redirect, flash, abort, request
from TaskApp import db
from TaskApp.tasks.forms import TaskForm
from flask_login import login_required, current_user
from TaskApp.models import Task

tasks=Blueprint('tasks', __name__)

#display all users tasks just title and small description not all and sort by due_date
@tasks.route("/tasks")
@login_required
def task_list():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.due_date.desc()).all()
    formatted_tasks = [{'title': task.title,
                        'description': task.description,
                        "task_id":task.task_id
                        } for task in tasks]
    return render_template("tasks.html", tasks=formatted_tasks)


#display the particular task and the information retated to it
@tasks.route('/tasks/<int:task_id>')
@login_required
def task(task_id):
    task = Task.query.get(task_id)
    formatted_task = {'title': task.title,
                      'description': task.description,
                      'importance': task.importance,
                      'due_date': task.due_date.strftime('%Y-%m-%d %H:%M'),
                      "task_id":task.task_id 
                      }
    return render_template('task.html', task=formatted_task)

#create task
@tasks.route("/tasks/create_task", methods=["GET","POST"])
@login_required
def create_task():
    form=TaskForm()
    if form.validate_on_submit():
        task=Task(title=form.title.data,
                  description=form.description.data,
                  due_date=form.due_date.data,
                  importance=form.importance.data,
                  user_id=current_user.id
                  )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("tasks.task_list", user_id=current_user.id)) 
    return render_template("create_task.html", title="New Task", legend="New Task", form=form)

#update task
@tasks.route("/task/<int:task_id>/update_task", methods=["GET","POST"])
@login_required
def update_task(task_id):
    task=Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    form=TaskForm()
    if form.validate_on_submit():
        task=Task(title=form.title.data,
                  description=form.description.data,
                  due_date=form.due_date.data,
                  importance=form.importance.data,
                  user_id=current_user.id
                  )
        db.session.add(task)
        db.session.commit()
        flash('Your Post Has Been Updated', 'success')
        return redirect(url_for("tasks.task_list", user_id=current_user.id))
    elif request.method == 'GET':
        form.title.data=task.title
        form.due_date.data=task.due_date
        form.description.data=task.description
        form.importance.data=task.importance

    return render_template("create_task.html", title="Update Task", legend="New Task", form=form)

#delete task
@tasks.route("/task/<int:task_id>/delete")
@login_required
def delete_task(task_id):
    task=Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Your Task Has Been Deleted', 'success')
    return redirect(url_for("tasks.task_list"))


