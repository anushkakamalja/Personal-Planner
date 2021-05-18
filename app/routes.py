# from wtforms.validators import Email
from app import app
from flask import render_template, request, url_for, redirect, abort
import flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask.helpers import flash
from app.models import Dashboard, Tasks, User, updateone

# from app.forms import VerifyUser
from flask_login import login_user, logout_user,login_required, current_user
from sqlalchemy.engine import url
from sqlalchemy.sql import exists
from sqlalchemy import func
# from app.email import send_email

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
    # id= user.id
    return redirect(url_for('dashboard'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    print(name)

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    User.add_user(new_user=new_user)

    return redirect(url_for('login'))


@app.route('/search',methods=['GET','POST'])
@login_required
def search():
    if request.method=='POST':
        # print(request.form)
        title=request.form['Search']
        # todos=Dashboard.query.filter_by(title=title).first()
        todos=Tasks.find_task(title=title)
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
        todo=Tasks.find_task(title=title)
        # print(todo.title)
        found_list=True
        # return redirect(url_for('main.dashboard',search_list=search_list,found_list=found_list))
        return render_template('task.html',todo=todo,found_list=found_list,project=project)
    else:
        todo=Tasks.query.filter_by(title=title).first()
        return render_template('task.html',todo=todo,found_list=found_list,project=project)

@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    if request.method=='POST':
        title=request.form['title']    
        todos=Dashboard(title=title,email=current_user.email)
        Dashboard.add_todo(todos=todos)
        print(current_user)
        email=current_user.email
        allTodo=Dashboard.query.filter(func.lower(Dashboard.email)==func.lower(current_user.email)).all()
        return redirect(url_for('dashboard'))

    else:
        print(current_user.email)
        allTodo=Dashboard.query.filter(func.lower(Dashboard.email)==func.lower(current_user.email)).all()
        return render_template('dashboard.html', allTodo=allTodo)


@app.route('/tasks/<project>', methods=['GET','POST'])
@login_required
def tasks(project):
    if request.method=='POST':
        title=request.form['title']
        print(current_user.email)
        todo=Tasks(title=title,complete=False, project=project)
        Tasks.add_todo(todos=todo)
        # incomplete=Tasks.query.filter_by(complete=False).all()
        # complete=Tasks.query.filter_by(complete=True).all()
        return redirect(url_for('tasks',project=project))
    else:
        # exists = db.session.query(Dashboard.title).filter_by(title=).first() is not None
        exists = Tasks.check_tasks(title=Dashboard.title, project=project)
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
        Tasks.remove_task(todo_list=todo_list)
        return redirect(url_for('dashboard'))

@app.route('/delete/<project>/<int:sno>')
@login_required
def delete(sno,project):
        todo=Tasks.query.filter_by(sno=sno).first()
        Tasks.remove_task(todo)
        return redirect(url_for('tasks',project=project))

@app.route('/complete/<project>/<int:sno>')
@login_required
def complete(sno,project):
    todo=Tasks.query.filter_by(sno=sno).first()
    todo.complete=True
    Tasks.task_completed(status=todo.complete)
    return redirect(url_for('tasks',project=project))
    

@app.route('/incomplete/<project>/<int:sno>')
@login_required
def incomplete(sno,project):
    todo=Tasks.query.filter_by(sno=sno).first()
    todo.complete=False
    Tasks.task_completed(status=todo.complete)
    return redirect(url_for('tasks',project=project))

@app.route('/update/<project>/<int:sno>',methods=['GET','POST'])
def updatetask(sno,project):
    if request.method=='POST':
        title=request.form['title']
        todo=Tasks.query.filter_by(sno=sno).first()
        todo.title=title
        Tasks.add_todo(todo)
        return redirect(url_for('tasks',project=project))
    else:
        todo=Tasks.query.filter_by(sno=sno).first()
        return render_template('updatetask.html',todo=todo, project=project)


@app.route('/profile',methods=["GET","POST"])
@login_required
def profile():
    id=current_user.id
    print(id)
    user=User.query.filter_by(id=id).first()
    print(user)
    name=user.name
    email=user.email
    password=user.password
    print(email)
        # user.name=name
    

    if request.method=="POST":
        user=User.query.filter_by(id=id).first()
        print(user)
        name=request.form["name"]
        email=request.form["email"]
        print(name, email)
        updateone(id=id,name=name,email=email)
        return redirect(url_for('profile'))




    return render_template('profile.html', name=current_user.name, email=email)

    
# @app.route('/send_mail',methods=['POST','GET'])
# def send_mail():
#     form = VerifyUser()
#     if form.validate_on_submit():
#         email = form.data["email"]
#         is_user = User.check_user(email)
#         send_email(email)
#         return redirect(url_for('login'))
#     return render_template("send_mail.html", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))