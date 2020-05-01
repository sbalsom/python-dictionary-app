from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User
from app.api.errors import error_response
from datetime import datetime, timedelta

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)

@basic_auth.error_handler
def basic_auth_error():
    return error_response(401)

@token_auth.verify_token
def verify_token(access_token):

    # if g.current_user.access_token_expiration > now + timedelta(seconds=60) and g.current_user.refresh_token_expiration < now:
    #     access_token = g.current_user.get_access_token()
    #     db.session.commit()
  # TODO : check the validity of the refresh token and provide a new access token

  # todo : maybe in this method I can check refresh token then check access token
    # if access token is expired first use refresh token to update access token then check access token
    #  TODO : this method would allow me to spoof my identity !!
    g.current_user = User.check_access_token(access_token) if access_token else None
    return g.current_user is not None

@token_auth.error_handler
def token_auth_error():
    return error_response(401)
