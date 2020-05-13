from app import db, app
from models import Quote, Anime, Character
import pickle

with open('db.pickle', 'rb') as d:
    quotes = pickle.load(d)

def main():
    with app.app_context():
        db.create_all()

    with app.app_context():
        for quote in quotes:
            print(quote.get_tags())
            create_quote(quote)
        db.session.commit()

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
        tags=quote.get_tags_list()
    ))

if __name__ == '__main__':
    main()
