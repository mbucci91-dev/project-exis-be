from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from keys import *

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = TABLE_USER
    
    id = db.Column(KEY_USER_ID, db.Integer, primary_key=True)
    username = db.Column(KEY_USERNAME, db.String(80), unique=True, nullable=False)
    password = db.Column(KEY_PASSWORD, db.String(120), nullable=False)
    status = db.Column(KEY_STATUS, db.String(20), nullable=False, default=S_USER_ACTIVE)
    secret_pin = db.Column(KEY_SECRET_PIN, db.String(5), nullable=False)
    
    cards = db.relationship('Card', backref='owner', lazy=True)

class Card(db.Model):
    __tablename__ = TABLE_CARD

    id = db.Column(KEY_CARD_ID, db.Integer, primary_key=True)
    pan = db.Column(KEY_PAN, db.String(16), nullable=False)
    holder = db.Column(KEY_HOLDER, db.String(50), nullable=False)
    exp_date = db.Column(KEY_EXP_DATE, db.String(5), nullable=False)
    user_id = db.Column(KEY_USER_ID_FK, db.Integer, db.ForeignKey(f"{TABLE_USER}.{KEY_USER_ID}"), nullable=False)
    status = db.Column(KEY_STATUS, db.String(20), nullable=False, default=S_CARD_ACTIVE)
    cvv = db.Column(KEY_CVV, db.String(4), nullable=False)
    
    movements = db.relationship('Movement', backref='card', lazy=True)

class Movement(db.Model):
    __tablename__ = TABLE_MOVEMENT

    id = db.Column(KEY_MOV_ID, db.Integer, primary_key=True)
    date = db.Column(KEY_DATE, db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(KEY_AMOUNT, db.Float, nullable=False)
    description = db.Column(KEY_DESCRIPTION, db.String(200), nullable=False)
    card_id = db.Column(KEY_CARD_ID_FK, db.Integer, db.ForeignKey(f"{TABLE_CARD}.{KEY_CARD_ID}"), nullable=False)