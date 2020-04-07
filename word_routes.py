from flask_restful import Resource, reqparse
from word import Word

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)

class Words(Resource):
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
