class DictionaryMethods():

    def __repr__(self):
        return '<Dictionary {}: {} by {}>'.format(self.id, self.name, self.user_id)

    def __init__(self, name, user_id):
        self.user_id = user_id
        self.name = name

    @classmethod
    def as_json_collection(cls, dictionaries):
        response = {
            'dictionaries': [dictionary.as_json() for dictionary in dictionaries]
        }

        return response

    def as_json(self):
        response = {
          '_id': self.id,
          '_user_id': self.user_id,
          'name': self.name,
          'owned_by': self.user.username
        }
        return response

