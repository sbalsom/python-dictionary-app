class UserWordMethods():
    def __repr__(self):
        return '<UserWord {}: by {} in {}>'.format(self.word.name, self.user.username, self.dictionary.name)

    def __init__(self, word_id, dictionary_id, user_id):
        self.word_id = word_id,
        self.dictionary_id = dictionary_id,
        self.user_id = user_id

    def as_json(self):
        response = {
          '_user_id': self.user_id,
          '_dictionary_id': self.dictionary_id,
          '_word_id': self.word_id,
          'word':self.word.as_json(),
        }
        return response
