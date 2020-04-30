class DictionaryMethods():
    def as_json(self):
      response = {
        '_id': self.id,
        '_user_id': self.user_id,
        'name': self.name,
        'user': self.user.as_json()
      }
      return response
