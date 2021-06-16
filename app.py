from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from src.forms import PeopleForm, WelcomeForm

from data import ACTORS
from modules import get_names, get_actor, get_id
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
    name = db.Column(db.String, primary_key=True)
    diet = db.Column(db.String)
    isConfirmed = db.Column(db.Boolean, default = False)

    def __init__(self, pid, group_name, name, diet, isConfirmed):
        self.pid = pid
        self.group_name = group_name
        self.name = name
        self.diet = diet
        self.isConfirmed = isConfirmed

def formatList(people, id):
    l = []
    for person in people:
        d = {}
        query = Invitation.query.with_entities(Invitation.name).filter_by(pid=id, name=person['people_name']).all()
        d['people_name'] = query[0]['name']
        query = Invitation.query.with_entities(Invitation.diet).filter_by(pid=id, name=person['people_name']).all()
        d['diet'] = query[0]['diet']
        query = Invitation.query.with_entities(Invitation.isConfirmed).filter_by(pid=id, name=person['people_name']).all()
        d['check'] = query[0]['isConfirmed']
        l.append(d)
    return l

# all Flask routes below

@app.route('/', methods=['GET', 'POST'])
def index():
    names = get_names(ACTORS)
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
            id = get_id(ACTORS, name)
            # redirect the browser to another route and template
            return redirect( url_for('actor', id=id) )
        else:
            message = "That actor is not in our database."
    return render_template('index.html', names=names, form=form, message=message)

@app.route('/actor/<id>', methods=['GET', 'POST'])
def actor(id):
    # run function to get actor data based on the id in the path
    id, group_name, people = get_actor(ACTORS, id)
    if Invitation.query.filter_by(pid=id).first() is None: # if not in database
        form = PeopleForm(people=people)
    else: # already in database
        l = formatList(people, id)
        form = PeopleForm(people=l)
    if form.is_submitted():
        if Invitation.query.filter_by(pid=id).first() is None:
            for person in form.data["people"]:
                pid = id
                name = person['people_name']
                diet = person['diet']
                isConfirmed = person['check']
                record = Invitation(pid, group_name, name, diet, isConfirmed)
                db.session.add(record)
                db.session.commit()
        else:
            for person in form.data["people"]:
                invitation = Invitation.query.filter(Invitation.pid == id, Invitation.name == person['people_name']).first()
                invitation.pid = id
                invitation.name = person['people_name']
                invitation.diet = person['diet']
                invitation.isConfirmed = person['check']
                db.session.commit()
            
        return redirect( url_for('success'))
    if group_name == "Unknown":
        # redirect the browser to the error template
        return render_template('404.html'), 404
    else:
        # pass all the data for the selected actor to the template
        return render_template('actor.html', id=id, name=group_name, people=people, form=form)

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
