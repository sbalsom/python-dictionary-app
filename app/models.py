from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

# user_words = db.Table('user_words',
#   db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
#   db.Column('word_id', db.Integer, db.ForeignKey('words.id'), primary_key=True),
#   db.Column('dictionary_id', db.Integer, db.ForeignKey('dictionaries.id'), primary_key=True),
#   db.Column('date_created', db.DateTime, default=db.func.current_timestamp()),
#   db.Column('date_modified', db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
# )

class UserWord(db.Model):
  __tablename__ = 'user_words'
  # __table_args__ = tuple(UniqueConstraint('word_id', 'dictionary_id',
  #                          name='word_dictionary_unique_constraint'))

  word_id = db.Column(db.Integer, db.ForeignKey('words.id'), primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  dictionary_id = db.Column(db.Integer, db.ForeignKey('dictionaries.id'), primary_key=True)
  date_created  = db.Column(db.DateTime, index=True, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    dictionaries = db.relationship('Dictionary', backref='owner', lazy='dynamic')
    date_created  = db.Column(db.DateTime, index=True, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    words = db.relationship('Word', secondary='user_words', lazy='subquery', backref=db.backref('users'))

    def __repr__(self):
        return '<User {}: {}>'.format(self.id, self.username)

    def set_password(self, password):
      self.password_hash = generate_password_hash(password)

    def check_password(self, password):
      return check_password_hash(self.password_hash, password)

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

    def as_json(self):
      response = {
        "id": self.id,
        "username": self.username
      }
      return response

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
      words = []
      for w in self.words:
        words.append(w.as_json())
      response = {
        "id": self.id,
        "name": self.name,
        "owner": self.owner.as_json(),
        "words": words
      }
      return response

class Word(db.Model):
  __tablename__ = 'words'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120))
  dictionary_id = db.Column(db.Integer, db.ForeignKey('dictionaries.id'))
  date_created  = db.Column(db.DateTime, index=True, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())


  def __repr__(self):
        return '<Word {}: {}>'.format(self.id, self.name)

  def as_json(self):
    response = {
      "id": self.id,
      "name": self.name
    }
    return response


