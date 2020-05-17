class UserWordMethods():
    def __repr__(self):
        return '<UserWord {}: by {} in {}>'.format(self.word.name, self.user.username, self.dictionary.name)

    def __init__(self, word_id, dictionary_id, user_id):
        self.word_id = word_id,
        self.dictionary_id = dictionary_id,
        self.user_id = user_id

    @classmethod
    def as_json_collection(cls, words):
        response = {
              'words': [word.as_json() for word in words]
          }

        return response

    def as_json(self):
        response = {
          '_user_id': self.user_id,
          '_dictionary_id': self.dictionary_id,
          '_word_id': self.word_id,
          'word':self.word.as_json(),
          'description': self.description,
          'translations': [t.sentence for t in self.translations]
        }
        return response
