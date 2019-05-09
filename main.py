from app import App, db
from app.models import User, Post, Role

#
@App.shell_context_processor   # register the function as a shell context
def make_shell_context():           # ... when you run 'flask shell'
    return {'db': db, 'User': User, 'Post': Post, 'Role': Role}
