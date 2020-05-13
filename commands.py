from app import db, app
from models import Quote, Anime, Character

def main():
    with app.app_context():
        db.create_all()

    with app.app_context():
        for quote in quotes:
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

    db.session(Quote(
        anime=anime_model,
        character=character_model,
        quote=quote.get_quote(),
        tags=quote.get_tags()
    ))

if __name__ == '__main__':
    main()
