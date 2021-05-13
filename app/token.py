from app import db
from app.models import User
import jwt
from app import app
from datetime import datetime, timedelta

def get_user_token(email):
    token = jwt.encode({'email': email, 'exp': datetime.utcnow() + timedelta(minutes=10),'iat': datetime.utcnow()},app.config['RESET_TOKEN_SECRET'], algorithm='HS256')
    return token
