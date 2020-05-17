

class TranslationMethods:
    def __init__(self, word_id, dictionary_id, sentence):
        self.word_id = word_id
        self.dictionary_id = dictionary_id
        self.sentence = sentence

    def __repr__(self):
        return '<Translation: {}>'.format(self.sentence)

    def as_json(self):
        response = {
          '_id': self.id,
          'sentence': self.sentence
        }
        return response
