from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField, SubmitField, SelectField,DateTimeLocalField
from wtforms.validators import DataRequired

#Form for task created to be used in html to get values and add to models
class TaskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    due_date = DateTimeLocalField("Due Date", validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    importance = SelectField("Importance", choices=[('Not really important', 'Not really important'), ('Important', 'Important'), ('Very Important', 'Very Important')], coerce=str, validators=[DataRequired()])
    complexity = SelectField("Complexity", choices=[('Easy', 'Easy'), ('Ok', 'Ok'), ('Very Complex', 'Very Complex')], coerce=str, validators=[DataRequired()])
    submit=SubmitField("Submit")