from wtforms.fields.html5 import DateField
from wtforms.fields.html5 import TimeField
from flask_wtf import FlaskForm
import mongoengine.errors
from wtforms.validators import URL, Email, DataRequired
from wtforms.fields.html5 import URLField
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, FileField, BooleanField

class ProfileForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()]) 
    image = FileField("Image") 
    submit = SubmitField('Post')

class SleepForm(FlaskForm):
    day = DateField('Day', format='%Y-%m-%d',validators=[DataRequired()])
    hours = IntegerField('Hours Slept', validators=[DataRequired()])
    disturbances = IntegerField('Disturbances', validators=[DataRequired()])
    quality = IntegerField('Quality', validators=[DataRequired()])
    notes = StringField()
    

class PetForm(FlaskForm):
    name = StringField()
    type = SelectField('Pet Type', choices=[(1, "Fox"), (2, "Wolf"), (3, "Cat")])
    submit = SubmitField('Post')
