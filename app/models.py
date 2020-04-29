# from datetime import datetime
# from app import db

from flask import url_for

from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import base64
from datetime import datetime, timedelta
import os
# from app.api.words.word import Test
# import app.api.words

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

class APIMixin(object):
    @staticmethod
    def paginated_collection(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        response = {
            'followed_users': [item.as_json() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return response

    @staticmethod
    def collection(items):
        response = {
            'items': [item.as_json() for item in items],
            '_meta': {
                'total_items': len(items)
            }
        }

        return response

class UserWord(db.Model):
    __tablename__ = 'user_words'
    __table_args__ = (db.UniqueConstraint('word_id', 'dictionary_id', name='_dictionary_word_combo_id'),
                       )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), primary_key=True, autoincrement=False, index=True, nullable=False)
    dictionary_id = db.Column(db.Integer, db.ForeignKey('dictionaries.id'), primary_key=True, autoincrement=False, index=True, nullable=False)
    date_created  = db.Column(db.DateTime, index=True, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# how to have word inherit from a class i import from another module
class Word(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    dictionary_id = db.Column(db.Integer, db.ForeignKey('dictionaries.id'))
    date_created  = db.Column(db.DateTime, index=True, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                         onupdate=db.func.current_timestamp())

# TODO : These methods can be written on a class called WordSerializer and called that way from routes
    def __repr__(self):
        return '<Word {}: {}>'.format(self.id, self.name)

    def from_json(self, data):
        for field in ['name']:
            if field in data:
                setattr(self, field, data[field])


class Dictionary(db.Model):
    __tablename__ = 'dictionaries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_created  = db.Column(db.DateTime, index=True, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())

    words = db.relationship('Word', backref='dictionary', lazy='dynamic')
    def __repr__(self):
        return '<Dictionary {}: {}, user_id: {}>'.format(self.id, self.name, self.user_id)

    def as_json(self):
        response = {
          'id': self.id,
          'name': self.name,
          'owner': self.owner.as_json(),
          '_link': url_for('dictionaries.show', id=self.id)
        }
        return response

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    about_me = db.Column(db.String(140))
    password_hash = db.Column(db.String(128))
    dictionaries = db.relationship('Dictionary', backref='owner', lazy='dynamic')
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    date_created  = db.Column(db.DateTime, index=True, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    words = db.relationship('Word', secondary='user_words', primaryjoin=id == UserWord.user_id, secondaryjoin=UserWord.word_id == Word.id, lazy='subquery', backref=db.backref('users'), foreign_keys=[UserWord.user_id, UserWord.word_id])

    def __repr__(self):
        return '<User {}: {}>'.format(self.id, self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def follow(self, user):
        if not self.is_following(user):
          self.followed.append(user)

    def unfollow(self,user):
        if self.is_following(user):
          self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
              followers.c.followed_id == user.id).count() > 0

    def friend_highlights(self):
        # TODO : only the last ten or so
        return UserWord.query.join(followers, (followers.c.followed_id == UserWord.user_id)).filter(followers.c.follower_id == self.id).order_by(UserWord.date_created.desc())
        pass

    def as_json(self, include_email=False):
        response = {
          'id': self.id,
          'username': self.username,
          'follower_count': self.followers.count(),
          'followed_count': self.followed.count(),
          '_links': {
            'self': url_for('users.show', id=self.id),
            'followers': url_for('users.followers', id=self.id),
            'followed': url_for('users.followed', id=self.id),
          }
        }

        if include_email:
          response['email'] = self.email
        return response

    def from_json(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

