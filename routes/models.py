# app/models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TravelData(db.Model):
    __tablename__ = 'travel_data'
    id = db.Column(db.Integer, primary_key=True)
    t_title = db.Column(db.String(100))
    t_location = db.Column(db.String(100))
    human_number = db.Column(db.Integer)
    overview = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    username = db.Column(db.String(100))
    details = db.relationship('TravelDetail', backref='travel', lazy=True)

class TravelDetail(db.Model):
    __tablename__ = 'travel_details'
    id = db.Column(db.Integer, primary_key=True)
    travel_id = db.Column(db.Integer, db.ForeignKey('travel_data.id'), nullable=False)
    day_number = db.Column(db.Integer)
    detail_name = db.Column(db.String(100))
    detail_text = db.Column(db.Text)
    visit_time = db.Column(db.Time)
    location_url = db.Column(db.String(255))
