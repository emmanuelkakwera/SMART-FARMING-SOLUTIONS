from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    full_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(10), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    farms = db.relationship('Farm', backref='owner', lazy=True)
    soil_records = db.relationship('SoilRecord', backref='user', lazy=True)
    animal_health = db.relationship('AnimalHealth', backref='user', lazy=True)


class Farm(db.Model):
    __tablename__ = 'farms'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    farm_name = db.Column(db.String(100), nullable=False)
    farm_size = db.Column(db.Float, nullable=False)
    farm_type = db.Column(db.String(20), nullable=False)
    soil_type = db.Column(db.String(50))
    location_coords = db.Column(db.String(100))
    main_crops = db.Column(db.Text)
    livestock_types = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    soil_records = db.relationship('SoilRecord', backref='farm', lazy=True)
    animal_health = db.relationship('AnimalHealth', backref='farm', lazy=True)


class SoilRecord(db.Model):
    __tablename__ = 'soil_records'

    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    test_date = db.Column(db.DateTime, default=datetime.utcnow)
    ph_level = db.Column(db.Float)
    nitrogen = db.Column(db.Float)
    phosphorus = db.Column(db.Float)
    potassium = db.Column(db.Float)
    organic_matter = db.Column(db.Float)
    recommendations = db.Column(db.Text)
    notes = db.Column(db.Text)


class AnimalHealth(db.Model):
    __tablename__ = 'animal_health'

    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    animal_type = db.Column(db.String(50), nullable=False)
    symptoms = db.Column(db.Text)
    disease_diagnosed = db.Column(db.String(100))
    treatment_applied = db.Column(db.Text)
    treatment_date = db.Column(db.DateTime, default=datetime.utcnow)
    recovery_status = db.Column(db.String(20))
    notes = db.Column(db.Text)