from flask import request, jsonify, json
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.auth import auth
#  TODO : setup email for password reset
# from app.auth.email import send_password_reset_email

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

@login.unauthorized_handler
def unauthorized():
    return 'Not authorized.', 401

@auth.route('/register', methods=['POST'])
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

@auth.route('/login', methods=['POST'])
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

@auth.route('/logout')
def logout():
  logout_user()
  return 'Successfully logged out.', 200
