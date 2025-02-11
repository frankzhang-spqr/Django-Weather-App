from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    favorite_cities = db.Column(db.JSON, default=list, nullable=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.set_password(password)
        self.favorite_cities = []

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_favorite_city(self, city):
        if self.favorite_cities is None:
            self.favorite_cities = []
        if city not in self.favorite_cities:
            self.favorite_cities.append(city)
            db.session.commit()

    def remove_favorite_city(self, city):
        if self.favorite_cities and city in self.favorite_cities:
            self.favorite_cities.remove(city)
            db.session.commit()

def init_db(app):
    """Initialize the database with proper settings based on environment"""
    # Set the database URI based on environment
    if os.environ.get('DATABASE_URL'):
        # Handle potential "postgres://" format in DATABASE_URL
        database_url = os.environ.get('DATABASE_URL')
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # SQLite for development
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weather.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize SQLAlchemy with the app
    db.init_app(app)
    
    # Create tables within app context
    with app.app_context():
        db.create_all()
        
    return db
