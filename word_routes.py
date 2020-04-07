from flask_restful import Resource, reqparse
from word import Word

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)

class Words(Resource):
  def get(self):
    return [w.json() for w in Word.query.all()]

  def post(self):
    data = parser.parse_args()
    word = Word(data["name"])
    word.save()
    return word.json(), 201

class WordInstance(Resource):
  def get(self, id):
    word = Word.find_by_id(id)
    if word:
      return word.json()
    else:
      return {"error": "Not found"}, 404

  def put(self, id):
    word = Word.find_by_id(id)
    data = parser.parse_args()
    if word:
      word.name = data['name']
      word.save()
      return word.json()
    else:
      return {"error": "Not found"}, 404

  def delete(self, id):
    word = Word.find_by_id(id)
    if word:
      word.destroy()
      return 'the word has been deleted'
    else:
      return {"error": "Not found"}, 404

