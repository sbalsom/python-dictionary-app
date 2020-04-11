from app import app, db, login
from flask_login import current_user, login_user, logout_user, login_required
from flask import request
from app.models import User
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
      return 'User already exists'
  return 'Please check your registration details and try again.', 422

@app.route('/login', methods=['POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  username = request.json['username']
  password = request.json['password']
  user = User.query.filter_by(username=username).first()
  if user is None:
    return 'User does not exist.', 401
  elif not user.check_password(password):
    return 'Incorrect password', 401
  elif user.check_password(password):
    login_user(user, remember=request.args.get('remember_me'))
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
