from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FormField, FieldList, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired


# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used
class WelcomeForm(FlaskForm):
    name = IntegerField('Einladungsnummer/Invitation ID : ', validators=[DataRequired()])
    submit = SubmitField('Weiter')

class PersonForm(FlaskForm):
    guest_name = StringField(validators = [DataRequired()])
    isConfirmed = BooleanField()
    diet = SelectField( choices=[('Alles'), ('Vegan'), ('Vegetarisch')])

class ExtrasForm(FlaskForm):
    music_choice_1 = StringField(default="Erster Musikwunsch")
    music_choice_2 = StringField(default="Zweiter Musikwunsch")
    music_choice_3 = StringField(default="Dritter Musikwunsch")
    shuttle_service = BooleanField()
    special_wishes = TextAreaField(default="Sonstiges?\nKinderhochsitz?")


class InviteForm(FlaskForm):
    people = FieldList(FormField(PersonForm), min_entries = 0)
    extras = FormField(ExtrasForm)
    submit = SubmitField('Submit')