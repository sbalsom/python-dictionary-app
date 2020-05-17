

class TranslationMethods:
    def __init__(word_id, dictionary_id, sentence, password, about_me='', new_user=False):
        self.word_id = word_id
        self.dictionary_id = dictionary_id
        self.sentence = sentence

    def __repr__(self):
        return '<Translation: {}>'.format(self.sentence)
