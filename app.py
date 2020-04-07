from flask import Flask
from db import db
from flask_restful import Api
from word_routes import Words, WordInstance
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

# @app.route('/')
# def home():
#   return "Home page"

api.add_resource(Words, '/words')
api.add_resource(WordInstance, '/words/<id>')

db.init_app(app)

if __name__ == '__main__':
  app.run(port=5000)

