from wtforms.validators import Email
from app import app, mail
from flask import Blueprint, render_template, request, url_for, redirect, abort
import flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask.helpers import flash
from app.models import Dashboard, Tasks, User
from app import db

from app.forms import VerifyUser
from flask_login import login_user, logout_user,login_required, current_user
from sqlalchemy.engine import url
from sqlalchemy.sql import exists
from sqlalchemy import func
from app.email import send_email

@app.route('/')
@app.route('/landing_page')
@app.route('/index')
def index():
    return render_template('landing_page.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('dashboard'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    if request.method=='POST':
        title=request.form['title']    
        todos=Dashboard(title=title)
        db.session.add(todos)
        db.session.commit()
        allTodo=Dashboard.query.all()
        return redirect(url_for('dashboard'))

    else:
        allTodo=Dashboard.query.all()
        return render_template('dashboard.html', allTodo=allTodo)


@app.route('/search',methods=['GET','POST'])
@login_required
def search():
    if request.method=='POST':
        # print(request.form)
        title=request.form['Search']
        # todos=Dashboard.query.filter_by(title=title).first()
        todos=db.session.query(Dashboard).filter(func.lower(Dashboard.title)==func.lower(title)).first()
        exist=todos is not None
        # print(todos.title)
        if exist:
            found_list=True
        # return redirect(url_for('main.dashboard',search_list=search_list,found_list=found_list))
            return render_template('dashboard.html',todos=todos,found_list=found_list)
        else:
            found_list=False
            return render_template('dashboard.html',todos=todos,found_list=found_list)
    else:
        todos=Dashboard.query.filter_by(title=title).first()
        return render_template('dashboard.html',todos=todos,found_list=found_list)

@app.route('/search/<project>',methods=['GET','POST'])
@login_required
def searchtask(project):
    if request.method=='POST':
        # print(request.form)
        title=request.form['Search']
        # todo=Tasks.query.filter_by(title=title).first()
        todo=db.session.query(Tasks).filter(func.lower(Tasks.title)==func.lower(title)).first()
        # print(todo.title)
        found_list=True
        # return redirect(url_for('main.dashboard',search_list=search_list,found_list=found_list))
        return render_template('task.html',todo=todo,found_list=found_list,project=project)
    else:
        todo=Tasks.query.filter_by(title=title).first()
        return render_template('task.html',todo=todo,found_list=found_list,project=project)

@app.route('/tasks/<project>', methods=['GET','POST'])
@login_required
def tasks(project):
    if request.method=='POST':
        title=request.form['title']
        todo=Tasks(title=title,complete=False, project=project)
        db.session.add(todo)
        db.session.commit()
        # incomplete=Tasks.query.filter_by(complete=False).all()
        # complete=Tasks.query.filter_by(complete=True).all()
        return redirect(url_for('tasks',project=project))
    else:
        # exists = db.session.query(Dashboard.title).filter_by(title=).first() is not None
        exists = db.session.query(Dashboard).filter(func.lower(Dashboard.title)==func.lower(project)).first() is not None
        if exists:
            incomplete=Tasks.query.filter_by(complete=False,project=project).all()
            complete=Tasks.query.filter_by(complete=True,project=project).all()
            return render_template('task.html', project=project, incomplete=incomplete, complete=complete)
        else:
            abort(404)

@app.route('/delete/<int:sno>')
@login_required
def remove(sno):
        todo_list=Dashboard.query.filter_by(sno=sno).first()
        db.session.delete(todo_list)
        db.session.commit()
        return redirect(url_for('dashboard'))

@app.route('/delete/<project>/<int:sno>')
@login_required
def delete(sno,project):
        todo=Tasks.query.filter_by(sno=sno).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for('tasks',project=project))

@app.route('/complete/<project>/<int:sno>')
@login_required
def complete(sno,project):
    todo=Tasks.query.filter_by(sno=sno).first()
    todo.complete=True
    db.session.commit()
    return redirect(url_for('tasks',project=project))
    

@app.route('/incomplete/<project>/<int:sno>')
@login_required
def incomplete(sno,project):
    todo=Tasks.query.filter_by(sno=sno).first()
    todo.complete=False
    db.session.commit()
    return redirect(url_for('tasks',project=project))

@app.route('/update/<project>/<int:sno>',methods=['GET','POST'])
def updatetask(sno,project):
    if request.method=='POST':
        title=request.form['title']
        todo=Tasks.query.filter_by(sno=sno).first()
        todo.title=title
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('main.tasks',project=project))
    else:
        todo=Tasks.query.filter_by(sno=sno).first()
        return render_template('updatetask.html',todo=todo, project=project)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

    
@app.route('/send_mail',methods=['POST','GET'])
def send_mail():
    form = VerifyUser()
    if form.validate_on_submit():
        email = form.data["email"]
        is_user = User.check_user(email)
        send_email(email)
        return redirect(url_for('login'))
    return render_template("send_mail.html", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))