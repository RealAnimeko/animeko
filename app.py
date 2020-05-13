from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

from models import db
import os

from models import Quote, Anime, Character

# Temp libs
import pickle

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db.init_app(app)

with open('db.pickle', 'rb') as d:
    quotes = pickle.load(d)

def create_quote(quote):
    anime = quote.get_anime()
    character = quote.get_character()

    anime_model = Anime(
        name=anime.get_name(),
        image=anime.get_image()
    )

    character_model = Character(
        name=anime.get_name(),
        image=anime.get_image()
    )

    db.session.add(Quote(
        anime=anime_model,
        character=character_model,
        quote=quote.get_quote(),
        tags=quote.get_tag()
    ))

for quote in quotes:
    print(quote.get_tag())
    create_quote(quote)
db.session.commit()

class GetRandomQuote(Resource):
    def get(self):

        json = []
        for quote in quotes:
            q = {}
            q['character'] = quote.get_character().get_name()
            q['quote'] = quote.get_quote()
            json.append(q)

        filters = [Quote.character.name.ilike("Lelouch Vi Brittana")]

        quotesDB = db.session.query(Quote).\
            filter(*filters)

        for quote in quotesDB:
            q = {}
            q['character'] = quote.character.name
            q['quote'] = quote.quote
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
