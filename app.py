from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import url

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Tasks(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)

def __repr__(self) -> str:
    return f"{self.sno}={self.title}"

class Dashboard(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)

def __repr__(self) -> str:
    return f"{self.sno}={self.title}"

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/my_account')
def my_account():
    return render_template('my_account.html')

@app.route('/login')
def login():
    return render_template('login.html')
    
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/tasks/<project>', methods=['GET','POST'])
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

@app.route('/dashboard', methods=['GET','POST'])
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
     

@app.route('/delete/<project>/<int:sno>')
def delete(sno,project):
        todo=Tasks.query.filter_by(sno=sno).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for('tasks',project=project))
        
# @app.route('/update/<project>/<int:sno>')
# def update(sno,project):
#         todo=Tasks.query.filter_by(sno=sno).first()
#         db.session.delete(todo)
#         db.session.commit()
#         return redirect(url_for('tasks',project=project))
if __name__=="__main__":
    app.run(debug=True)