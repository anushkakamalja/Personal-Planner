from flask import Flask, render_template
app=Flask(__name__)
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

@app.route('/tasks')
def tasks():
    return render_template('task.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
