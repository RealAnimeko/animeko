from anime import Anime
from character import Character
from quote import Quote
import pandas as pd
import re

import pickle

df = pd.read_csv("quote.csv")
print(df.head())

json = {}
# Anime, Quote, Name, Img, AnimeImg
for index, row in df.iterrows():
    anime, quote, html_quote, character, tags, img, animeImg = row[0], row[1], row[2], row[3], row[4], row[5],row[6]
    print(img)
    if not anime in json:
        json[anime] = {
            'characters': [],
            'image': animeImg
        }
        # print(anime)

    if not any(character in x for x in json[anime]['characters']):
        json[anime]['characters'].append({
            character: {
                'quotes': [],
                'image': img
            }        })

    for i in json[anime]['characters']:
        character_json = i
        if character in i:
            # print(type(tags.split(',')))
            q = Quote(html_quote, tags.split(','), 0, 0)
            i[character]['quotes'].append(q)

ANIME = []
for anime_name in json:
    # print(json[anime_name]['image'])
    anime = Anime(anime_name, json[anime_name]['image'], [] , 0)
    for char in json[anime_name]['characters']:
        for character_name in char:
            quotes = char[character_name]['quotes']
            image = char[character_name]['image']
            character = Character(character_name, image, quotes, 0)

            anime.set_characters(character)

    ANIME.append(anime)

with open('db.pickle', 'wb') as db:
    pickle.dump(ANIME, db)
