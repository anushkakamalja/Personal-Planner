from flask_login import UserMixin
from sqlalchemy import func
from sqlalchemy.orm import backref
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True ) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    dashboard=db.relationship('Dashboard', backref='creator', lazy='dynamic')

    def add_user(new_user):
        db.session.add(new_user)
        db.session.commit()

    def check_user(email):
        user = User.query.filter_by(email=email).first()
        if user:
            return True
        return False

    def updateone( self, name, email):
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        db.session.commit()       



class Tasks(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    complete=db.Column(db.Boolean)
    project=db.Column(db.String(300))

    def add_todo(todos):
        print(todos)
        db.session.add(todos)
        db.session.commit()

    def find_task(title):
        return db.session.query(Dashboard).filter(func.lower(Dashboard.title)==func.lower(title)).first()

    def check_tasks(title,project):
        return db.session.query(Dashboard).filter(func.lower(Dashboard.title)==func.lower(project)).first() is not None

        
    def remove_task(todo_list):
        db.session.delete(todo_list)
        db.session.commit()
    
    def task_completed(todo):
        db.session.add(todo)
        db.session.commit()


def __repr__(self) -> str:
    return f"{self.sno}={self.title}"

class Dashboard(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))

    def add_todo(todos):
        print(todos)
        db.session.add(todos)
        db.session.commit()

    def find_task(title):
        return db.session.query(Dashboard).filter(func.lower(Dashboard.title)==func.lower(title)).first()

    def check_tasks(title,project):
        return db.session.query(Dashboard).filter(func.lower(Dashboard.title)==func.lower(project)).first() is not None

        
    def remove_task(todo_list):
        db.session.delete(todo_list)
        db.session.commit()
    
    def task_completed(status):
        if status == True:
            db.session.commit()

def __repr__(self) -> str:
    return f"{self.sno}={self.title}"


