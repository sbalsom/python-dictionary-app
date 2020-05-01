from flask import url_for
from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import base64
from datetime import datetime, timedelta
import os
from app.methods import w, uw, d, u

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

class Dictionary(d.DictionaryMethods, db.Model):
    __tablename__ = 'dictionaries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_created  = db.Column(db.DateTime, index=True, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())

    words = db.relationship('UserWord', back_populates='dictionary')

class UserWord(uw.UserWordMethods, db.Model):
    __tablename__ = 'user_words'
    __table_args__ = (db.UniqueConstraint('word_id', 'dictionary_id', name='_dictionary_word_combo_id'),
                       )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), primary_key=True, autoincrement=False, index=True, nullable=False)
    dictionary_id = db.Column(db.Integer, db.ForeignKey('dictionaries.id'), primary_key=True, autoincrement=False, index=True, nullable=False)
    date_created  = db.Column(db.DateTime, index=True, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    user = db.relationship("User", lazy="joined")
    word = db.relationship("Word", lazy="joined")
    dictionary = db.relationship("Dictionary", back_populates="words")

class Word(w.WordMethods, db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    dictionary_id = db.Column(db.Integer, db.ForeignKey('dictionaries.id'))
    date_created  = db.Column(db.DateTime, index=True, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                         onupdate=db.func.current_timestamp())

class User(u.UserMethods, UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    about_me = db.Column(db.String(140))
    password_hash = db.Column(db.String(128))
    dictionaries = db.relationship('Dictionary', backref='user', lazy='dynamic')
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

    def from_json(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

