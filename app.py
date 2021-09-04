from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap

from src.forms import InviteForm, WelcomeForm
from src.database.db import db
from src.database.models import Invitation, Extras

from preset_data import Invites
from src.io import get_pids, get_invitation_preset
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
db.init_app(app)

@app.route('/', methods=['GET'])
def index_get():
    # create new WelcomeForm
    form = WelcomeForm()
    message = ""
    return render_template('index.html', form=form, message=message)

@app.route('/', methods=['POST'])
def index_post():
    # get WelcomeFrom
    form = WelcomeForm()
    # get given entry as string
    entry = str(form.input.data)
    if entry in get_pids(Invites):
        # redirect the browser to another route and template
        return redirect( url_for('invite_get', id=entry) )
    else:
        message = "That ID is not known!"
        return render_template('index.html', form=form, message=message)


@app.route('/invite/<id>', methods=['GET'])
def invite_get(id):
    # check if invitation ID is in database:
    if Invitation.query.filter_by(pid=id).first() is None:
        # get default values from data.py
        _, group_name, list_of_people = get_invitation_preset(Invites, id)
        # if id not in valid
        if not id:
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
        extras_dict = Extras(id)
    else:
        extras_dict = Extras.query.filter_by(pid=id).first().to_dict()
    
    # create form which gets redered
    form = InviteForm(people=list_of_people, extras=extras_dict)
    
    return render_template('invite.html', id=id, form=form, group_name=group_name)

@app.route('/invite/<id>', methods=['POST'])
def invite_post(id):
    # handle guests
    form = InviteForm() # get form from post req, dont know how that works

    if Invitation.query.filter_by(pid=id).first() is None:
        # get needed preset data
        pid , group_name, people = get_invitation_preset(Invites, id)
        for person in people:
            # create new empty entry
            record = Invitation(pid, group_name)
            record.from_preset(person)
            db.session.add(record)
            db.session.commit()
    # get all people of the pid from data base
    persons_in_database = Invitation.query.filter_by(pid=id).all()
    for idx, person in enumerate(form.people): # iter through fields on form
        # get current entry, that should be modified
        invitation = Invitation.query.filter(Invitation.pid == id, Invitation.guest_name == persons_in_database[idx].guest_name).first()
        # modify the fields
        invitation.from_form(person)
        db.session.commit()

    # handle extras
    if Extras.query.filter_by(pid=id).first() is None: # if no extras in database, add to database
        record = Extras(id)
        db.session.add(record)
        db.session.commit()
    # get data from database
    record = Extras.query.filter_by(pid=id).first()
    # fill with data from webform
    record.from_form(form.extras)
    # commit changes to database
    db.session.commit()

    return redirect( url_for('success'))

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
    app.run(debug=True, host='0.0.0.0', port=80)
