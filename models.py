from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anime = db.relationship('Anime', backref=backref('quote', uselist=False))
    character = db.relationship('Character', backref=backref('quote', uselist=False))
    quote = db.Column(db.String())
    tag = db.Column(db.String(), uselist=False)

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anime_id = db.Column(db.Integer, db.ForeignKey('quote.id'))
    name = db.Column(db.String())
    image = db.Column(db.String())

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anime_id = db.Column(db.Integer, db.ForeignKey('quote.id'))
    name = db.Column(db.String())
    image = db.Column(db.String())

# def get(limit=1000):
#     return db.session.query(Article).order_by(Article.date_of_publication)
