from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Tasks(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    complete=db.Column(db.Boolean)
    project=db.Column(db.String(300))

def __repr__(self) -> str:
    return f"{self.sno}={self.title}"

class Dashboard(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)

def __repr__(self) -> str:
    return f"{self.sno}={self.title}"
