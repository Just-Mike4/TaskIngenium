from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField, DateTimeField,SubmitField, IntegerField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    title=StringField("Title", validators=[DataRequired()])
    description=TextAreaField("Description", validators=[DataRequired()])
    due_date=DateTimeField("Due_Date", validators=[DataRequired()])
    importance=IntegerField("Importance", validators=[DataRequired()])
    submit=SubmitField("Task")