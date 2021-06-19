from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from src.forms import ExtrasForm, InviteForm, WelcomeForm

from preset_data import Invites
from modules import get_names, get_invitation_preset, get_id
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

class Extras(db.Model):
    __tablename__ = 'extras'
    pid = db.Column(db.Integer, primary_key=True)
    music_choice_1 = db.Column(db.String)
    music_choice_2 = db.Column(db.String)
    music_choice_3 = db.Column(db.String)
    shuttle_service = db.Column(db.Boolean, default = False)
    special_wishes = db.Column(db.String)

    def __init__(self, pid):
        self.pid = pid
        self.music_choice_1 = "Erster Musikwunsch"
        self.music_choice_2 = "Zweiter Musikwunsch"
        self.music_choice_3 = "Dritter Musikwunsch"
        self.shuttle_service = False
        self.special_wishes = "Noch was?"

    def to_dict(self):
        d = {}
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                continue
            d[key] = value
        return d

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
            return redirect( url_for('invite_get', id=id) )
        else:
            message = "That actor is not in our database."
    return render_template('index.html', names=names, form=form, message=message)


@app.route('/invite/<id>', methods=['POST'])
def invite_post(id):
    ## submission of data
    # handle guests
    form = InviteForm() # get form from post req, dont know how that works
    if Invitation.query.filter_by(pid=id).first() is None:
        # get preset data
        _ , group_name, _ = get_invitation_preset(Invites, id)
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
        # get all people of the pid, needed to match the to be changed entry.
        people = Invitation.query.filter_by(pid=id).all()
        for idx, person in enumerate(form.data["people"]): # iter through fields on form
            # get current entry
            invitation = Invitation.query.filter(Invitation.pid == id, Invitation.guest_name == people[idx].guest_name).first()
            # modufy the fields
            invitation.guest_name = person['guest_name']
            invitation.diet = person['diet']
            invitation.isConfirmed = person['isConfirmed']
            # commit to database
            db.session.commit()
    # handle extras
    if Extras.query.filter_by(pid=id).first() is None:
        # if no extras in database
        record = Extras(id)
        record.music_choice_1 = form.extras.music_choice_1.data
        record.music_choice_2 = form.extras.music_choice_2.data
        record.music_choice_3 = form.extras.music_choice_3.data
        record.shuttle_service = form.extras.shuttle_service.data
        record.special_wishes = form.extras.special_wishes.data
        db.session.add(record)
        db.session.commit()
    else:
        record = Extras.query.filter_by(pid=id).first()
        record.music_choice_1 = form.extras.music_choice_1.data
        record.music_choice_2 = form.extras.music_choice_2.data
        record.music_choice_3 = form.extras.music_choice_3.data
        record.shuttle_service = form.extras.shuttle_service.data
        record.special_wishes = form.extras.special_wishes.data
        db.session.commit()

    return redirect( url_for('success'))

@app.route('/invite/<id>', methods=['GET'])
def invite_get(id):
    # run function to get actor data based on the id in the path

    # check if invitation ID is in database:
    if Invitation.query.filter_by(pid=id).first() is None:
        # get default values from data.py
        id, group_name, list_of_people = get_invitation_preset(Invites, id)
        # if id not in valid
        if not id:
            # redirect the browser to the error template
            return render_template('404.html'), 404

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

    # check if invitaion ID is in extras database:
    if Extras.query.filter_by(pid=id).first() is None:
        # create new form
        dic = Extras(id)
    else:
        dic = Extras.query.filter_by(pid=id).first().to_dict()
    
    form = InviteForm(people=list_of_people, extras=dic)


    
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
