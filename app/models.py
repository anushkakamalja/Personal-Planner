from flask_login import UserMixin
from sqlalchemy import func
from sqlalchemy.orm import backref
from . import db


class User(UserMixin, db.Model):
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True ) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    # tasks=db.relationship('Tasks', backref='user_email', lazy='dynamic')
    dashboard=db.relationship('Dashboard', backref='creator', lazy='dynamic')

    def add_user(new_user):
        db.session.add(new_user)
        db.session.commit()

    def check_user(email):
        user = User.query.filter_by(email=email).first()
        if user:
            return True
        return False


def updateone(id, name, email):
        # email="anushkakamalja@gmail.com"
        user = User.query.filter_by(id=id).first()
        user.name=name
        user.email = email
        db.session.commit()

# class ResetUser(UserMixin, db.Model):
#     email = db.Column(db.String(100), unique=True, primary_key=True)
#     token = db.Column(db.String(100))

class Tasks(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    complete=db.Column(db.Boolean)
    project=db.Column(db.String(300))
    # email=db.Column(db.String(300), db.ForeignKey('user.email'))

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

class Dashboard(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    email=db.Column(db.String(300), db.ForeignKey('user.email'))

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


# with app.app_context():
#     db.create_all()