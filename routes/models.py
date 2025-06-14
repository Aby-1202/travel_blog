from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from . import db

class TravelData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    t_title = db.Column(db.String(100))
    
class TravelData(db.Model):  # テーブル名：travel_data
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date)

class TravelDetail(db.Model):  # テーブル名：travel_detail
    id = db.Column(db.Integer, primary_key=True)
    travel_id = db.Column(db.Integer, db.ForeignKey('travel_data.id'))
    location = db.Column(db.String(100))
    memo = db.Column(db.Text)
