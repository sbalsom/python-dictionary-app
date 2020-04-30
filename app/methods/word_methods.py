class WordMethods():

    def __init__(self, name):
        self.name = name


    def __repr__(self):
        return '<Word {}: {}>'.format(self.id, self.name)

    @classmethod
    def as_json_collection(cls, words):
        response = {
              'words': [word.as_json() for word in words]
          }

        return response

    def as_json(self):
        response = {
          '_id': self.id,
          'name': self.name
        }
        return response
