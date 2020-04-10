from datetime import datetime
from app import db


class User(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    dictionary = db.relationship('Dictionary', backref='owner', lazy='dynamic')
    date_created  = db.Column(db.DateTime,  index=True, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())


    def __repr__(self):
        return '<User {}: {}>'.format(self.id, self.username)

    def set_password(self, password):
      self.password_hash = generate_password_hash(password)

    def check_password(self, password):
      return check_password_hash(self.password_hash, password)


class Dictionary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created  = db.Column(db.DateTime, index=True, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())

    words = db.relationship('Word', backref='dictionary', lazy='dynamic')
    def __repr__(self):
        return '<Dictionary {}: {}, user_id: {}>'.format(self.id, self.name, self.user_id)

class Word(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120))
  dictionary_id = db.Column(db.Integer, db.ForeignKey('dictionary.id'))
  date_created  = db.Column(db.DateTime, index=True, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())

  def __repr__(self):
        return '<Word {}: {}>'.format(self.id, self.name)
