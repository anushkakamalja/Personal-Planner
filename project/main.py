from flask import Blueprint, render_template, request, url_for, redirect
from .models import Dashboard
from .models import Tasks
from . import db
from flask_login import login_required, current_user
from sqlalchemy.engine import url

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('landing_page.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/landing_page')
def landing_page():
    return render_template('landing_page.html')


@main.route('/tasks/<project>', methods=['GET','POST'])
@login_required
def tasks(project):
    if request.method=='POST':
        title=request.form['title']
        todo=Tasks(title=title,complete=False)
        db.session.add(todo)
        db.session.commit()
        # incomplete=Tasks.query.filter_by(complete=False).all()
        # complete=Tasks.query.filter_by(complete=True).all()
        return redirect(url_for('main.tasks',project=project))
    else:
        incomplete=Tasks.query.filter_by(complete=False).all()
        complete=Tasks.query.filter_by(complete=True).all()
        return render_template('task.html', project=project, incomplete=incomplete, complete=complete)

@main.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    if request.method=='POST':
        title=request.form['title']    
        todo=Dashboard(title=title)
        db.session.add(todo)
        db.session.commit()
        allTodo=Dashboard.query.all()
        return redirect(url_for('main.dashboard'))
    else:
        allTodo=Dashboard.query.all()
        return render_template('dashboard.html', allTodo=allTodo)


@main.route('/delete/<int:sno>')
@login_required
def remove(sno):
        todo_list=Dashboard.query.filter_by(sno=sno).first()
        db.session.delete(todo_list)
        db.session.commit()
        return redirect(url_for('main.dashboard'))

@main.route('/update/<int:sno>',methods=['GET','POST'])
@login_required
def update(sno):
    if request.method=='POST':
        title=request.form['title']    
        todo_list=Dashboard.query.filter_by(sno=sno).first()
        todo_list.title=title
        db.session.add(todo_list)
        db.session.commit()
        allTodo=Dashboard.query.all()
        return redirect(url_for('main.dashboard'))
    else:
        todo_list=Dashboard.query.filter_by(sno=sno).first()
        return render_template('updateproject.html', todo_list=todo_list)


@main.route('/delete/<project>/<int:sno>')
@login_required
def delete(sno,project):
        todo=Tasks.query.filter_by(sno=sno).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for('main.tasks',project=project))

@main.route('/complete/<project>/<int:sno>')
@login_required
def complete(sno,project):
    todo=Tasks.query.filter_by(sno=sno).first()
    todo.complete=True
    db.session.commit()
    return redirect(url_for('main.tasks',project=project))
    

@main.route('/incomplete/<project>/<int:sno>')
@login_required
def incomplete(sno,project):
    todo=Tasks.query.filter_by(sno=sno).first()
    todo.complete=False
    db.session.commit()
    return redirect(url_for('main.tasks',project=project))

@main.route('/update/<project>/<int:sno>',methods=['GET','POST'])
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
