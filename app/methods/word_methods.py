class WordMethods():

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by


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
          'name': self.name,
          'created_by': self.created_by
        }
        return response
