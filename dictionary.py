from app import create_app, db
from app.models import User, Dictionary, Word

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Dictionary': Dictionary, 'Word': Word}
