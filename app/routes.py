from app import app, db, login
from flask_login import current_user, login_user, logout_user, login_required
from flask import request, jsonify, json
from app.models import User, Word
from sqlalchemy.exc import IntegrityError


@login.user_loader
def load_user(id):
  return User.query.get(int(id))

@login.unauthorized_handler
def unauthorized():
    return 'Not authorized.', 401

@app.route('/register', methods=['POST'])
def register():
  if current_user.is_authenticated:
    return 'You are already logged in.', 200
  username = request.json.get('username', False)
  email = request.json.get('email', False)
  password = request.json.get('password', False)
  if username and email and password:
    try:
      # do I need to do something to avoid sql injection here ?
      user = User(username=username, email=email)
      user.set_password(password)
      db.session.add(user)
      db.session.commit()
      return 'User {} successfully created !'.format(user.username)
    except IntegrityError:
      return 'User already exists', 422
  return 'Please check your registration details and try again.', 422

@app.route('/login', methods=['POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  username = request.json.get('username')
  password = request.json.get('password')
  user = User.query.filter_by(username=username).first()
  if user is None:
    return 'User does not exist.', 401
  elif not user.check_password(password):
    return 'Incorrect password', 401
  elif user.check_password(password):
    remember = request.json.get('remember_me', False)
    login_user(user, remember=remember)
    return 'Success.', 200

@app.route('/logout')
def logout():
  logout_user()
  return 'Successfully logged out.', 200

@app.route('/')
@app.route('/home')
@login_required
def home():
  return 'Welcome {}'.format(current_user.username)

@app.route('/my_dictionaries', methods=['GET'])
@login_required
def index():
  response = []
  for d in current_user.dictionaries:
    print(d.as_json())
    response.append(d.as_json())
  return jsonify(response)

@app.route('/my_dictionaries/<int:id>', methods=['GET'])
@login_required
def  show(id):
  dictionary = current_user.dictionaries.filter_by(id=id).first()
  if dictionary:
    return jsonify(dictionary.as_json())
  return 'Not found.', 404


# @app.route('/my_words/<int: id>', methods=['GET'])
# @login_required
# def  show():

@app.route('/<int:id>/my_words', methods=['POST'])
@login_required
def  create(id):
  # dictionary_id = request.json.get('dictionary_id')
  dictionary = current_user.dictionaries.filter_by(id=id).first()
  if dictionary:
    name = request.json.get('name')
    w = Word(name=name, dictionary_id=id)
    db.session.add(w)
    db.session.commit()
    return "'{}' successfully added to the dictionary: {}".format(w.name, dictionary.name)
  return 'Not found', 404

# @app.route('/my_words/<int: id>', methods=['PUT'])
# @login_required
# def  update():

# @app.route('/my_words/<int: id>', methods=['DELETE'])
# @login_required
# def  delete():

