class WordMethods():

    def as_json_collection(self, words):
        response = {
              'words': [self.as_json(word) for word in words]
          }

        return response

    def as_json(word):
        response = {
          'id': word.id,
          'name': word.name
        }
        return response

class Test():
    def from_json(self, data):
        for field in ['name']:
            if field in data:
                setattr(self, field, data[field])

    def say_hello():
        print("hello")


        #   def from_json(self, data):
