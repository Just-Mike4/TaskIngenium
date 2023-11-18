from flask import Blueprint, render_template, url_for, redirect, flash, abort
from TaskApp import db
from TaskApp.tasks.forms import TaskForm
from flask_login import login_required, current_user
from TaskApp.models import Task
tasks=Blueprint('tasks', __name__)

user_id=current_user.id

@tasks.route("/tasks")
@login_required
def tasks(user_id):
    if user_id == current_user.id:
        tasks=Task.query.order_by(Task.due_date.desc())
    return render_template("tasks.html", tasks=tasks)

@tasks.route('/task/<int:task_id>')
@login_required
def task(task_id):
    task=Task.query.get(task_id)
    return render_template('task.html', title=task.title, task=task)


@tasks.route("/task/create_task")
@login_required
def create_task():

    form=TaskForm()
    if form.validate_on_submit:
        task=Task(title=form.title.data,
                  description=form.description.data,
                  due_date=form.due_date.data,
                  importance=form.importance.data,
                  )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("tasks.tasks"))
    flash('Your Post Has Been Created', 'success')  
    return render_template("create_task.html")

@tasks.route("/task/update_task")
@login_required
def update_task():

    form=TaskForm()
    if form.validate_on_submit:
        task=Task(title=form.title.data,
                  description=form.description.data,
                  due_date=form.due_date.data,
                  importance=form.importance.data,
                  )
        db.session.add(task)
        db.session.commit()
        flash('Your Post Has Been Updated', 'success')
        return redirect(url_for("tasks.tasks"))
    return render_template("create_task.html")

@tasks.route("/task/<int:task_id>/<int:user_id>/delete")
@login_required
def delete_task(task_id, user_id):
    task=Task.query.get_or_404(task_id)
    if user_id != current_user:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Your Post Has Been Deleted', 'success')
    return redirect(url_for("tasks.tasks"))


