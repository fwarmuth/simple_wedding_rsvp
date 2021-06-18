from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from src.forms import InviteForm, WelcomeForm

from data import Invites
from modules import get_names, get_invite, get_id
import re
app = Flask(__name__)

# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'IAmARealSecret!!!!!!!!!!!!!!!!!!!!!!!!11'

db_name = 'rsvp.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Flask-Bootstrap requires this line
Bootstrap(app)

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

# Class representing the data structure model within tha database
class Invitation(db.Model):
    __tablename__ = 'invitation'
    pid = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String)
    guest_name = db.Column(db.String, primary_key=True)
    diet = db.Column(db.String)
    isConfirmed = db.Column(db.Boolean, default = False)

    def __init__(self, pid, group_name, guest_name, diet, isConfirmed):
        self.pid = pid
        self.group_name = group_name
        self.guest_name = guest_name
        self.diet = diet
        self.isConfirmed = isConfirmed
    
    def to_dict(self):
        d = {}
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                continue
            d[key] = value
        return d

class extras(db.Model):
    __tablename__ = 'extras'
    pid = db.Column(db.Integer, primary_key=True)
    music_choice_1 = db.Column(db.String)
    music_choice_2 = db.Column(db.String)
    music_choice_3 = db.column(db.String)
    shuttle_service = db.Column(db.Boolean, default = False)
    special_wishes = db.column(db.String)

    def __init__(self, pid):
        self.pid = pid
        self.music_choice_1 = ""
        self.music_choice_2 = ""
        self.music_choice_3 = ""
        self.shuttle_service = False
        self.special_wishes = ""




# all Flask routes below

@app.route('/', methods=['GET', 'POST'])
def index():
    names = get_names(Invites)
    print(names)
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = WelcomeForm()
    message = ""
    if form.validate_on_submit():
        name = int(form.name.data)
        if name in names:
            # empty the form field
            form.name.data = ""
            id = get_id(Invites, name)
            # redirect the browser to another route and template
            return redirect( url_for('invite', id=id) )
        else:
            message = "That actor is not in our database."
    return render_template('index.html', names=names, form=form, message=message)

@app.route('/invite/<id>', methods=['GET', 'POST'])
def invite(id):
    # run function to get actor data based on the id in the path

    # check if ID is in database:
    if Invitation.query.filter_by(pid=id).first() is None:
        # get default values from data.py
        id, group_name, people = get_invite(Invites, id)
        # if id not in valid
        if not id:
            # redirect the browser to the error template
            return render_template('404.html'), 404

        form = InviteForm(people=people)

    else: # already in database
        # get invite with pid and return all people
        people = Invitation.query.filter_by(pid=id).all()
        group_name = people[0].group_name
        # turn invitations to dicts
        list_of_people = []
        for person in people:
            # iter through invitations
            d = person.to_dict()
            list_of_people.append(d)

        form = InviteForm(people=list_of_people)
        # group_name = people[

    if form.is_submitted():
        if Invitation.query.filter_by(pid=id).first() is None:
            # first submision, add to database
            for person in form.data["people"]:
                pid = id
                name = person['guest_name']
                diet = person['diet']
                isConfirmed = person['isConfirmed']
                record = Invitation(pid, group_name, name, diet, isConfirmed)
                db.session.add(record)
                db.session.commit()
        else:
            # change existing entry
            for idx, person in enumerate(form.data["people"]): # iter through fields on form
                invitation = Invitation.query.filter(Invitation.pid == id, Invitation.guest_name == people[idx].guest_name).first()
                invitation.pid = id
                invitation.guest_name = person['guest_name']
                invitation.diet = person['diet']
                invitation.isConfirmed = person['isConfirmed']
                db.session.commit()

        return redirect( url_for('success'))
    
        # pass all the data for the selected actor to the template
    return render_template('invite.html', id=id, people=people, form=form, group_name=group_name)

@app.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('success.html')

# 2 routes to handle errors - they have templates too

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# keep this as is
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1337)
