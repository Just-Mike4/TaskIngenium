from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField, SubmitField, SelectField,DateTimeLocalField
from wtforms.validators import DataRequired

#Form for task created to be used in html to get values and add to models
class TaskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    due_date = DateTimeLocalField("Due_Date", validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    importance = SelectField("Importance", choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], coerce=int, validators=[DataRequired()])
    submit=SubmitField("Submit")