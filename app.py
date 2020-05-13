from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

from models import db
import os

from anime import Anime
from character import Character
from quote import Quote

# Temp libs
import pickle

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db.init_app(app)

with open('db.pickle', 'rb') as d:
    quotes = pickle.load(d)

class GetRandomQuote(Resource):
    def get(self):

        json = []
        for quote in quotes:
            q = {}
            q['character'] = quote.get_character().get_name()
            q['quote'] = quote.get_quote()
            json.append(q)

        return { 'quotes': json }

api.add_resource(GetRandomQuote, '/quote')

class getQuoteByAnime(Resource):
    def get(self):

        json = []
        for quote in quotes:
            q = {}
            q['character'] = quote.get_character().get_name()
            q['quote'] = quote.get_quote()
            json.append(q)

        return { 'quotes': json }

api.add_resource(getQuoteByAnime, '/anime')

if __name__ == "__main__":
    app.run(debug=True, port=8000)
