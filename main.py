from app import app, db
from app import routes, models

@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": models.User, "Dashboard": models.Dashboard, "Tasks": models.Tasks}