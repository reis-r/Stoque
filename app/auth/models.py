from app import db
from flask_login import UserMixin

class User(UserMixin, db.Document):
    meta = {'collection': 'users'}
    username = db.StringField(max_length=80)
    password = db.StringField(min_length=8)
