from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import sqlalchemy.types as types

class HTMLType(types.TypeDecorator):
    impl = types.String
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(150))
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    subtitle = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    date_edited = db.Column(db.DateTime)

    
    