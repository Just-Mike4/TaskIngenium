from flask import Blueprint, render_template

tasks=Blueprint('tasks', __name__)


@tasks.route('/task')
def home():
    return render_template('task.html')

