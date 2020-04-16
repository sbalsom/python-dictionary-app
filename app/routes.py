# from flask import current_app
# from app import db, login
# from flask import request, jsonify, json
# from app.models import User, Word
# from sqlalchemy.exc import IntegrityError

# @current_app.route('/')
# @app.route('/home')
# @login_required
# def home():
#   return 'Welcome {}'.format(current_user.username)

# @current_app.route('/my_dictionaries', methods=['GET'])
# @login_required
# def index():
#   response = []
#   for d in current_user.dictionaries:
#     print(d.as_json())
#     response.append(d.as_json())
#   return jsonify(response)

# @current_app.route('/my_dictionaries/<int:id>', methods=['GET'])
# @login_required
# def  show(id):
#   dictionary = current_user.dictionaries.filter_by(id=id).first()
#   if dictionary:
#     return jsonify(dictionary.as_json())
#   return 'Not found.', 404


# # @app.route('/my_words/<int: id>', methods=['GET'])
# # @login_required
# # def  show():

# @current_app.route('/<int:id>/my_words', methods=['POST'])
# @login_required
# def  create(id):
#   # dictionary_id = request.json.get('dictionary_id')
#   dictionary = current_user.dictionaries.filter_by(id=id).first()
#   if dictionary:
#     name = request.json.get('name')
#     w = Word(name=name, dictionary_id=id)
#     db.session.add(w)
#     db.session.commit()
#     return "'{}' successfully added to the dictionary: {}".format(w.name, dictionary.name)
#   return 'Not found', 404

# # @app.route('/my_words/<int: id>', methods=['PUT'])
# # @login_required
# # def  update():

# # @app.route('/my_words/<int: id>', methods=['DELETE'])
# # @login_required
# # def  delete():

