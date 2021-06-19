from src.forms import PersonForm, ExtrasForm

from src.database.db import db

# Class representing the data structure model within tha database
class Invitation(db.Model):
    __tablename__ = 'invitation'
    pid = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String)
    guest_name = db.Column(db.String, primary_key=True)
    diet = db.Column(db.String)
    isConfirmed = db.Column(db.Boolean, default = False)

    def __init__(self, pid, group_name):
        self.pid = pid
        self.group_name = group_name
        self.guest_name = "NoName"
        self.diet = "Alles"
        self.isConfirmed = False
    
    def to_dict(self):
        d = {}
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                continue
            d[key] = value
        return d
    
    def from_preset(self, d: dict):
        self.guest_name = d["guest_name"]
        self.diet = "Alles"
        self.isConfirmed = False 

    def from_form(self, form: PersonForm):
        self.guest_name = form.guest_name.data
        self.diet = form.diet.data
        self.isConfirmed = form.isConfirmed.data

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

    def from_form(self, form: ExtrasForm):
        #TODO comment docstring
        self.music_choice_1 = form.music_choice_1.data
        self.music_choice_2 = form.music_choice_2.data
        self.music_choice_3 = form.music_choice_3.data
        self.shuttle_service = form.shuttle_service.data
        self.special_wishes = form.special_wishes.data
