from db import db

class Word(db.Model):
  __tablename__ = 'words'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)

  def __init__(self, name):
    self.name = name

  def json(self):
    return {"id": self.id, "name": self.name}

  def save(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def find_by_id(cls, id):
    return cls.query.filter_by(id=id).first()
