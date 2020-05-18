from app import db, app
from models import Quote, Anime, Character
import pickle

with open('db.pickle', 'rb') as d:
    animes = pickle.load(d)

def main():
    with app.app_context():
        db.create_all()

    with app.app_context():
        for anime in animes:
            print(anime)
            create_quote(anime)
        db.session.commit()

def create_quote(anime):

    characters_models = []
    characters = anime.get_characters()
    for character in characters:
        quotes_models = []
        quotes = character.get_quotes()
        for quote in quotes:
            print(type(quote.get_tags()))
            quotes_models.append(Quote(
                quote=quote.get_quote(),
                tags=quote.get_tags(),
                views=quote.get_views(),
                likes=quote.get_likes()
            ))

        characters_models.append(Character(
            name=character.get_name(),
            image=character.get_image(),
            quotes=quotes_models,
            views=character.get_views()
        ))


    db.session.add(Anime(
        name=anime.get_name(),
        image=anime.get_image(),
        characters=characters_models,
        views=anime.get_views()
    ))

    print("{} added".format(anime.get_name()))

if __name__ == '__main__':
    main()
