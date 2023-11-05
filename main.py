from app import App, db
from app.models import User, Post, Role

# register the function as a shell context
@App.shell_context_processor   

# when you run 'flask shell'
def make_shell_context():           
    return {'db': db, 'User': User, 'Post': Post, 'Role': Role}
