from flask_mail import Message
from app import mail
# from app import db
# from app.models import User

def send_email(email):
    msg = Message("test-mail", sender="no-reply", recipients=[email])
    msg.body = "You've registered."
    msg.html = "<h1>hi</h1>"
    mail.send(msg)
    