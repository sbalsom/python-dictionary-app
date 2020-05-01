from werkzeug.security import generate_password_hash, check_password_hash
import base64
from datetime import datetime, timedelta
import os
from app import db

class UserMethods():
    def __repr__(self):
        return '<User {}: {}>'.format(self.id, self.username)

    def __init__(self, email, username, password, about_me='', new_user=False):
        self.email = email
        self.username = username
        self.about_me = about_me
        if new_user:
            self.set_password(password)

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

    def get_access_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.access_token and self.access_token_expiration > now + timedelta(seconds=60):
            return self.access_token
        self.access_token = base64.b64encode(os.urandom(50)).decode('utf-8', 'ignore')
        self.access_token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.access_token

    def get_refresh_token(self, expires_in=28800):
        now = datetime.utcnow()
        if self.refresh_token and self.refresh_token_expiration > now + timedelta(seconds=60):
            return self.refresh_token
        self.refresh_token = base64.b64encode(os.urandom(50)).decode('utf-8', 'ignore')
        self.refresh_token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.refresh_token

    def revoke_access_token(self):
        self.access_token_expiration = datetime.utcnow() - timedelta(seconds=1)

    def revoke_refresh_token(self):
        self.refresh_token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @classmethod
    def check_access_token(cls, access_token):
        user = cls.query.filter_by(access_token=access_token).first()
        if user is None:
            return None
        elif user.access_token_expiration < datetime.utcnow() and user.refresh_token_expiration >= datetime.utcnow():
            # refresh_token = user.refresh_token
            # user = cls.check_refresh_token(refresh_token)
            user.get_access_token()
            db.session.commit()
            return user
        elif user.access_token_expiration >= datetime.utcnow():
            return user
        else:
            return None

    @classmethod
    def check_refresh_token(cls, refresh_token):
      #  TODO : does this allow one user to replace themself with another ?
        user = cls.query.filter_by(refresh_token=refresh_token).first()
        if user is None or user.refresh_token_expiration < datetime.utcnow():
            return None
        return user

#  TODO : a method to return a user's followers
# 'follower_count': self.followers.count(),
#           'followed_count': self.followed.count(),
#           '_links': {
#             'self': url_for('users.show', id=self.id),
#             'followers': url_for('users.followers', id=self.id),
#             'followed': url_for('users.followed', id=self.id),
#           }

#     def get_token(self, expires_in=3600):
#         now = datetime.utcnow()
#         if self.token and self.token_expiration > now + timedelta(seconds=60):
#             return self.token
#         self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
#         self.token_expiration = now + timedelta(seconds=expires_in)
#         db.session.add(self)
#         return self.token

#     def revoke_token(self):
#         self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

#     @staticmethod
#     def check_token(token):
#         user = User.query.filter_by(token=token).first()
#         if user is None or user.token_expiration < datetime.utcnow():
#             return None
#         return user




