
class UserWordMethods():
    def __repr__(self):
      return '<UserWord {}: by {} in {}>'.format(self.word.name, self.user.username, self.dictionary.name)
