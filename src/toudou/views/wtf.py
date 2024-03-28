from flask_wtf import FlaskForm
from wtforms import FileField, HiddenField, SelectField, SubmitField, StringField, BooleanField, DateField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileField, FileAllowed

from uuid import UUID

from toudou.models import getNotCompletedToudous, convert_to_tuple_list

class DeleteToudouForm(FlaskForm):
    toudou_ID = HiddenField()
    submit = SubmitField("X")

class CreateToudouForm(FlaskForm):
    name = StringField("Your toudou's name :", validators=[DataRequired()])
    due_checkbox = BooleanField("Does your toudou have a deadline?")
    due = DateField("Due :", validators=[Optional()])
    submit = SubmitField("Submit")

class CompleteToudouForm(FlaskForm):
    id = SelectField('Select a toudou', validators=[DataRequired()], coerce=UUID)
    submit = SubmitField('Submit')

class ModifyToudouForm(FlaskForm):
    id = SelectField('Select a toudou', validators=[DataRequired()], coerce=UUID)
    tname = StringField('New toudou name', validators=[DataRequired()])
    due = DateField('New toudou\'s due', validators=[Optional()])
    complete = SelectField('Completed', choices=[('False', 'No'), ('True', 'Yes')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class UploadForm(FlaskForm):
    file = FileField("Your CSV file :", validators=[DataRequired(), FileAllowed(['csv'])])
    submit = SubmitField("Upload")
