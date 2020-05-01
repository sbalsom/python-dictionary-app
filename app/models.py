from app import db
# import os
from app.methods import w, uw, u, d
# from app.api.dictionaries import d

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

class User(u.UserMethods, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    about_me = db.Column(db.String(140))
    password_hash = db.Column(db.String(128))
    dictionaries = db.relationship('Dictionary', backref='user', lazy='dynamic')
    access_token = db.Column(db.String(200), index=True, unique=True)
    access_token_expiration = db.Column(db.DateTime)
    refresh_token = db.Column(db.String(200), index=True, unique=True)
    refresh_token_expiration = db.Column(db.DateTime)
    date_created  = db.Column(db.DateTime, index=True, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    words = db.relationship('Word', secondary='user_words', primaryjoin=id == UserWord.user_id, secondaryjoin=UserWord.word_id == Word.id, lazy='subquery', backref=db.backref('users'), foreign_keys=[UserWord.user_id, UserWord.word_id])


# unneeded import stuff maybe i need elsewhere :
# from flask import url_for
# from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin
# import base64
# from datetime import datetime, timedelta
# UserMixin
