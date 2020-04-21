from flask import jsonify, request, url_for, g, abort
from app import db
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.api.user_words import bp

# from app.api.user_words.user_word import UserWord
from app.models import User, Word, Dictionary, UserWord
# from app.api.dictionaries.dictionary import Dictionary
# from app.api.words.word import Word


@bp.route('/words', methods=['GET'])
@token_auth.login_required
def index():
    data = g.current_user.words
    print(data)
    # data = UserWord.query.join(Word).filter(UserWord.user_id == g.current_user.id).all()
    # print(data)
    # todo : call .as_json on each (collection method)
    return jsonify(Word.collection(data))

    # return UserWord.query.join(followers, (followers.c.followed_id == UserWord.user_id)).filter(followers.c.follower_id == self.id).order_by(UserWord.date_created.desc())
    #     pass

@bp.route('/words/<int:id>', methods=['GET'])
@token_auth.login_required
def show(id):
    return jsonify(UserWord.query.get_or_404(id).as_json())

@bp.route('/words', methods=['POST'])
@token_auth.login_required
def create():
    data = request.get_json() or {}
    dictionary = Dictionary.query.get(data['dictionary_id'])
    if dictionary in g.current_user.dictionaries:
        dictionary_id = dictionary.id
    else:
      # Or return bad request ?
      abort(403)
    if 'name' not in data:
        return bad_request('word cannot be blank')
    if Word.query.filter_by(name=data['name']).first():
      word = Word.query.filter_by(name=data['name']).first()
    else:
      word = Word(name=data['name'])
      db.session.add(word)
      db.session.commit()
    user_word = UserWord(word_id=word.id, dictionary_id=dictionary_id, user_id=g.current_user.id)
    db.session.add(user_word)
    db.session.commit()
    response = jsonify(word.as_json())
    response.status_code = 201
    response.headers['Location'] = url_for('words.show', id=word.id)
    return response

@bp.route('/words/<int:id>', methods=['PUT'])
@token_auth.login_required
def update(id):
    pass

@bp.route('/words/<int:id>', methods=['DELETE'])
@token_auth.login_required
def destroy(id):
    pass
