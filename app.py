from flask import Flask, render_template, request, send_from_directory
# from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import or_, desc
from sqlalchemy.sql import func
from sqlalchemy.orm import load_only
import random
import requests
import re
from datetime import datetime
import markdown

from models import db
import os

from models import Quote, Anime, Character
from global_var import *

app = Flask(__name__)
app.url_map.strict_slashes = False
url = 'https://z5208980.github.io/animeko/#' # 'https://animeko.herokuapp.com'
# url = '*'
cors = CORS(app, resources={r"/*": {'origins': url}})

os.environ['DATABASE_URL'] = 'postgresql://pniqfgxbqkqetu:6ecba25eebbfb5f164f03e9b6082e377558bde0517614b55f9beb896b73b9794@ec2-18-213-176-229.compute-1.amazonaws.com:5432/d8spdda2p97kqe'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db.init_app(app)

def get_random_quotes(total):
    quotes = Quote.query.order_by(func.random()).limit(total).all()
    character_ids = [quote.character_id for quote in quotes]
    characters = Character.query.filter(Character.id.in_(character_ids)).all()

    character_json = {}
    for character in characters:
        character_json[str(character.id)] = {
            'name': character.name,
            'image': character.image
        }

    ret = []
    for quote in quotes:
        char_id = str(quote.character_id)
        ret.append({
            'quote': quote.quote,
            'character': character_json[char_id]['name'],
            'image': character_json[char_id]['image']
        })

    return ret
    # return [{'quote': quote.quote, 'character': character.name, 'image': character.image} for quote, character in zip(quotes, characters)]

def get_quote_of_the_day():
    url = 'https://graph.facebook.com/101129927954000/posts'
    params = {
        'method':'GET',
        'version':'v7.0',
        'path':'101129927954000%2Fposts',
        'classic':'0',
        'access_token':'EAAHkCZAp4QgMBANeC4PSHRUEp3vmbsJcs2INCnZCXuKfylZCYI7AGlstaMOJ1WnhAIigufMdb9vQ4t5aYHM9NFeysZCRrGIRFPikpziAmprhULuqJBvaPN3aszpri4cTHHr6PLoF0ZBZAfeZAYWALuZB5DjD6pnfxi0FjMW4ZBnzoywZDZD'
    }
    r = requests.get(url, params=params)
    json = r.json()

    posts = {
        'data': []
    }
    quote_of_the_day = {}
    for post in json['data']:
        if 'message' in post:
            ids = post['id'].split('_')
            data = {
                'id': ids[0],
                'story_fbid': ids[1]
            }
            if not 'quote_of_the_day' in posts:
                posts['quote_of_the_day'] = data
            elif re.search("Quote of the day #[0-9]".lower(), post['message'].lower()):
                posts['data'].append(data)

    return posts

def get_popular_anime(total):
    animes = Anime.query.order_by(Anime.views.desc()).limit(total).all()

    ret = []
    for anime in animes:
        ret.append({
            'name': anime.name,
            'image': anime.image,
            'views': anime.views
        })
        print("{}, {}".format(anime.name, anime.views))
    return ret
    # return [{'name': anime.name, 'image': anime.image, 'views': anime.views} for anime in animes]

# Array of anime names
list_api = {
    'title': 'API.AnimeNameList',
    'description': markdown.markdown(
        'Returns an `array` of available anime list that contains quotes.'
    ),
    'requestMethod': 'GET',
    'endpoint': '/list',
    'parameters': [

    ],
    'schema': {
        'responseContentType': 'application/json',
        'schema': [
            { 'param': 'data', 'type': 'array', 'description': markdown.markdown('List of all available searchable anime titles')}
        ]
    },
    'response': [
        { 'statusCode': 200, 'description': 'list of anime names' }
    ],
    'example': {
        'url': '/list',
        'ret': '''
    {
        "data": [
            "3-gatsu no Lion",
            "5 Centimeters Per Second",
            "A Place Further Than The Universe",
            "Akame Ga Kill",
            "Angel Beats!",
            "Assassination Classroom",
            "Attack on Titan",
            "Avatar",
            "Barakamon",
            "Beyond the Boundary",
            "Black Clover",
            ...
            ]
    }
        '''
    }
}
@app.route('/list', methods=['GET'])
def anime_name_list():
    ret = { 'data': anime_list }
    return ret

random_quotes_api = {
    'title': 'API.QuoteByRandom',
    'description': '',
    'requestMethod': 'GET',
    'endpoint': '/quotes/random',
    'schema': {
        'responseContentType': 'application/json',
        'schema': [
            { 'param': 'data', 'type': 'array', 'description': 'List of n quotes randomised from the database. See <a href="#TYPE.QUOTE">TYPE.QUOTE</a> for schema.'},
        ]
    },
    'response': [
        { 'statusCode': 200, 'description': 'list of anime names' }
    ],
    'example': {
        'url': '/quotes/random',
        'ret': '''
    {
        "data": [
            {
                "character": "Shigeo Kageyama",
                "image": "t0so4552ue0rkil/mob_psycho_shigeo.png",
                "quote": "I don\u2019t want to see anyone else <span class=\"text-lightred\">hurting</span> people, or anyone else getting <span class=\"text-lightred\">hurt</span>."
            },
            ...
        ]
    },
    '''
    }
}
@app.route('/quotes/random')
def generate_random_quotes():
    quotes = get_random_quotes(20)
    if quotes:
        return {'data': quotes, 'status': 200}, 200, {'Access-Control-Allow-Origin': url}
    else:
        return {'data': [], 'status': 404}, 404, {'Access-Control-Allow-Origin': url}

anime_quotes_api = {
    'title': 'API.QuoteByAnime',
    'description': 'Returns a JSON response of quotes from the given anime titles.',
    'requestMethod': 'GET',
    'endpoint': '/anime?name={titleOfAnime}',
    'parameters': [
        { 'param': 'title', 'optional': False, 'description': markdown.markdown('Input a list of anime titles with the delimiter `,`' )}
    ],
    'schema': {
        'responseContentType': 'application/json',
        'schema': [
            { 'param': 'character', 'type': 'array', 'description': 'List of all characters from the inputted anime. See See <a href="#TYPE.CHARACTER">TYPE.CHARACTER</a> for schema.'},
            { 'param': 'image', 'type': 'string', 'description': 'URL for the image of the anime title.'},
            { 'param': 'name', 'type': 'string', 'description': 'The name of the anime.'},
            { 'param': 'tags', 'type': 'array', 'description': 'List of tags relevant to the quote.'},
            { 'param': 'total_quotes', 'type': 'int', 'description': 'The total number of quotes from all the characters in the anime.'},
            { 'param': 'views', 'type': 'int', 'description': 'The total number of views for the anime.'},

        ]
    },
    'response': [
        { 'statusCode': 200, 'description': 'a JSON of characters from the anime with their respected quotes' }
    ],
    'example': {
        'url': '/anime?name=avatar',
        'ret': '''
    {
        "characters": [
            {
                "image": "g76iwd8tr5okmnc/avatar_the_last_airbender_aang.png",
                "name": "Aang",
                "quotes": [
                    {
                        "id": 78,
                        "likes": 0,
                        "quote": "The past can be a great <span class='text-orange'>teacher</span>.",
                        "tags": [
                            "motivational",
                            ...
                            ],
                        "views": 0
                    },
                    ...
            },
            ...
        ],
        "image": "tv364a19lxbcthl/avatar_the_last_airbender.png",
        "name": "Avatar",
        "tags": [
            "life",
            "change",
            "philosophical",
            "motivatonal",
            "live",
            "motivational"
        ],
        "total_quotes": 11,
        "views": 10
    }
    '''
    }
}

character_type = {
    'id': 'TYPE.CHARACTER',
    'schema': [
        { 'param': 'image', 'type': 'string', 'description': 'URL for the image of the character.'},
        { 'param': 'name', 'type': 'string', 'description': 'The name of the anime character.'},
        { 'param': 'quotes', 'type': 'array', 'description': 'List of all available quotes. See <a href="#TYPE.QUOTE">TYPE.QUOTE</a> for schema.'}
    ]
}

quote_type = {
    'id': 'TYPE.QUOTE',
    'schema': [
        { 'param': 'id', 'type': 'int', 'description': 'The unique id for the quote'},
        { 'param': 'likes', 'type': 'int', 'description': 'The amount of likes for a given quote.'},
        { 'param': 'quote', 'type': 'array', 'description': 'HTML version of the quote.'},
        { 'param': 'tags', 'type': 'array', 'description': 'List of tags relevant to the quote.'},
        { 'param': 'views', 'type': 'int', 'description': 'The amount of views on the given quote.'}
    ]
}

@app.route('/anime', methods=['GET', 'POST'])
def anime():
    if 'name' in request.args:
        anime = Anime.query.filter(Anime.name.ilike(request.args['name'])).first()
        if anime:
            anime.views += 1
            db.session.commit()

            a = {}
            a['name'] = anime.name
            a['image'] = anime.image
            a['characters'] = []
            a['total_quotes'] = 0
            a['tags'] = []
            for character in anime.characters:
                a['total_quotes'] += len(character.quotes)
                c = {}
                c['name'] = character.name
                c['image'] = character.image
                c['quotes'] = []
                for quote in character.quotes:
                    a['tags'].extend(quote.tags)
                    q = {}
                    q['id'] = quote.id
                    q['quote'] = quote.quote
                    q['tags'] = quote.tags
                    q['likes'] = quote.likes
                    q['views'] = quote.views
                    c['quotes'].append(q)
                c['views'] = character.views
                a['characters'].append(c)
            a['tags'] = list(set(a['tags']))
            a['views'] = anime.views

            print(a)
            return a
    return {'data': [], 'status': 404}, 404, {'Access-Control-Allow-Origin': url}


@app.route('/')
def index():
    doc = {
        'data': [
            list_api,
            random_quotes_api,
            anime_quotes_api
        ],
        'type': [
            character_type,
            quote_type
        ],
        'base': url
    }
    return render_template('index.html', doc=doc)

@app.route('/api/upvote', methods=['POST'])
def upvote():
    if request.method == 'POST':
        quote = Quote.query.get(request.args.get('id'))
        quote.likes += 1
        db.session.commit()
    return {'likes': quote.likes, 'status': 200}, 200, {'Access-Control-Allow-Origin': url}

@app.route('/api/downvote', methods=['POST'])
def downvote():
    if request.method == 'POST':
        quote = Quote.query.get(request.args.get('id'))
        if(quote.likes <= 0):
            quote.likes = 0
        else:
            quote.likes -= 1
        db.session.commit()
    return {'likes': quote.likes, 'status': 200}, 200, {'Access-Control-Allow-Origin': url}

# favicon display
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

if __name__ == "__main__":
    app.run(debug=True, port=8000)
