from werkzeug.security import generate_password_hash, check_password_hash
import base64
from datetime import datetime, timedelta
import os
from app import db
# from flask_jwt import JWT, jwt_required, current_identity
# from werkzeug.security import safe_str_cmp

class UserMethods():
    def __init__(self, email, username, password, about_me='', new_user=False):
        self.email = email
        self.username = username
        self.about_me = about_me
        if new_user:
            self.set_password(password)

    def __repr__(self):
        return '<User {}: {}>'.format(self.id, self.username)

    @classmethod
    def as_json_collection(cls, users):
        response = {
              'users': [user.as_json() for user in users]
        }

        return response

    def as_json(self, include_email=False):
        response = {
          '_id': self.id,
          'username': self.username,
          'about_me': self.about_me,

        }

        if include_email:
          response['email'] = self.email
        return response

    def follow(self, user):
        if not self.is_following(user):
          self.followed.append(user)

    def unfollow(self,user):
        if self.is_following(user):
          self.followed.remove(user)

    def friend_highlights(self):
        # TODO : only the last ten or so
        return UserWord.query.join(followers, (followers.c.followed_id == UserWord.user_id)).filter(followers.c.follower_id == self.id).order_by(UserWord.date_created.desc())
        pass

    def is_following(self, user):
        return self.followed.filter(
              followers.c.followed_id == user.id).count() > 0

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



