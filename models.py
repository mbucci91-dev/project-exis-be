from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    cards = db.relationship('Card', backref='owner', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pan = db.Column(db.String(16), nullable=False)
    holder = db.Column(db.String(50), nullable=False)
    exp_date = db.Column(db.String(5), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movements = db.relationship('Movement', backref='card', lazy=True)

class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)