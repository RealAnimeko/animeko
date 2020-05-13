from app import db, app
from .models import Quote, Anime, Character

def create_tables():
    with app.app_context():
        db.create_all()
