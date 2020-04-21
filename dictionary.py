from app import create_app, db
# from app.api.dictionaries.dictionary import Dictionary
from app.models import followers, User, UserWord, Dictionary, Word
# from app.api.user_words.user_word import UserWord
# from app.api.words.word import Word
# from app.api.users.user import User
# import app.api.users.user
# from app.models import User

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
    'db': db,
    'User': User,
    'Dictionary': Dictionary,
    'Word': Word,
    'UserWord': UserWord,
    'followers' : followers
    }
