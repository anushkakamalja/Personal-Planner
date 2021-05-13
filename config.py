import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY=os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS=os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
    RESET_TOKEN_SECRET=os.environ.get("RESET_TOKEN_SECRET")
    MAIL_SERVER=os.environ.get("MAIL_SERVER")
    MAIL_PORT=os.environ.get("MAIL_PORT")
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD")
    MAIL_SUPPRESS_SEND=False
    # MAIL_USE_SSL=False