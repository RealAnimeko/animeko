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

from models import db
import os

from models import Quote, Anime, Character
from global_var import *

app = Flask(__name__)
app.url_map.strict_slashes = False
# url = 'https://animeko.herokuapp.com'
url = '*'
cors = CORS(app, resources={r"/*": {'origins': url}})

os.environ['DATABASE_URL'] = 'postgres://pniqfgxbqkqetu:6ecba25eebbfb5f164f03e9b6082e377558bde0517614b55f9beb896b73b9794@ec2-18-213-176-229.compute-1.amazonaws.com:5432/d8spdda2p97kqe'
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

@app.route('/')
def index():
    popular_animes = get_popular_anime(6)
    quote_of_the_day = get_random_quotes(1).pop(0)
    print(quote_of_the_day)
    return render_template('index.html',
        total_quotes=total_quotes,
        popular_animes=popular_animes,
        quote_of_the_day=quote_of_the_day)

@app.route('/quote')
def quote():
    return render_template('quoteByRandom.html')

@app.route('/generate_random_quotes')
def generate_random_quotes():
    quotes = get_random_quotes(20)
    if quotes:
        return {'results': quotes, 'status': 200}, 200, {'Access-Control-Allow-Origin': url}
    else:
        return {'results': [], 'status': 404}, 404, {'Access-Control-Allow-Origin': url}

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
            return render_template('quotesByAnime.html', anime=a)
    return render_template('anime.html', animes=anime_list)

@app.route('/about')
def about():
    about = []
    faq = {
      "faq": [
        {
            "question": "Why does it load slowly sometimes?",
            "answer": "The main reason we load slowly, it that we are hosting on a free server called Heruko. For you who don't know Heroku, basically the free tier will put my site to sleep, everytime it is not used for a period of time. Meaning when someone accesses Animeko whilst the its sleeping, then it need time to awake up and load the entire backend server up. As time progresses and milestones are reached, then maybe we move to other services.",

        }, {
            "question": "Can I request a quote to be put up?",
            "answer": "Yes, all you need to do is email our enquiry email, and if it not available and appropaite than we'll put it up. We also keep an author which is your instagram andit will display under the quotes.",
        }]
    }
    return render_template('about.html', faq=faq, nav_change="#2e92ee")

@app.route('/quote_of_the_day')
def quote_of_the_day():
    posts = get_quote_of_the_day()
    return render_template('quoteOfTheDay.html', posts=posts)

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

##### Error Handling #####
@app.errorhandler(404)
def page_not_found(e):
    err = {
        'status': 404,
        'message': 'Sorry, the page does not exist. Maybe the URL is typed incorrectly'
    }
    return render_template('err.html', err=err), err['status']

@app.errorhandler(400)
def page_not_found(e):
    err = {
        'status': 400,
        'message': 'Sorry, No results'
    }
    return render_template('err.html', err=err), err['status']

@app.errorhandler(500)
def page_not_found(e):
    err = {
        'status': 500,
        'message': 'Sorry, Internal Server Error. This is our end thats not working.'
    }
    return render_template('err.html', err=err), err['status']

# favicon display
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

if __name__ == "__main__":
    app.run(debug=True, port=8000)
