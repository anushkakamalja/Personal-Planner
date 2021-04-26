from flask import Blueprint, render_template, request, url_for
from .models import Dashboard
from .models import Tasks
from . import db
from flask_login import login_required, current_user
from sqlalchemy.engine import url

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('base.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/tasks/<project>', methods=['GET','POST'])
@login_required
def tasks(project):
    if request.method=='POST':
        title=request.form['title']
        todo=Tasks(title=title)
        db.session.add(todo)
        db.session.commit()
        allTodo=Tasks.query.all()
        return redirect(url_for('tasks',project=project))
    else:
        allTodo=Tasks.query.all()
        return render_template('task.html', project=project, allTodo=allTodo)

@main.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    if request.method=='POST':
        title=request.form['title']    
        todo=Dashboard(title=title)
        db.session.add(todo)
        db.session.commit()
        allTodo=Dashboard.query.all()
        return render_template('dashboard.html', allTodo=allTodo)
    else:
        allTodo=Dashboard.query.all()
        return render_template('dashboard.html', allTodo=allTodo)
     

@main.route('/delete/<project>/<int:sno>')
@login_required
def delete(sno,project):
        todo=Tasks.query.filter_by(sno=sno).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for('tasks',project=project))