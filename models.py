from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    image = db.Column(db.String())
    characters = db.relationship('Character', backref='anime')
    views = db.Column(db.Integer())

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.id'))
    name = db.Column(db.String())
    image = db.Column(db.String())
    quotes = db.relationship('Quote', backref='character')
    views = db.Column(db.Integer())

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    quote = db.Column(db.Text())
    # tags = db.Column(db.String())
    tags = db.Column(db.ARRAY(db.String()))
    views = db.Column(db.Integer())
    likes = db.Column(db.Integer())
