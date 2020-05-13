from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anime = db.relationship('Anime', uselist=False, backref='quote')
    character = db.relationship('Character', uselist=False, backref="quote")
    quote = db.Column(db.Text())
    tags = db.Column(db.String())

# Many quotes in one Anime
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
