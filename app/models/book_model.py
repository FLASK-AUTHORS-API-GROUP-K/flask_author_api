from app.extensions import db
from datetime import datetime

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    price = db.Column(db.String(50))
    description = db.Column(db.String(100))
    isbn = db.Column(db.String(50))
    image = db.Column(db.String(50))
    no_of_pages = db.Column(db.String(50))
    price_unit = db.Column(db.String(50))
    publication_year = db.Column(db.String(50))
    genre = db.Column(db.String(50))
    specialisation = db.Column(db.String(50))
    created_at = db.Column(db.DateTime,  default = datetime.now())
    updated_at = db.Column(db.DateTime,  onupdate = datetime.now())
        

    
    
    def __init__(self, id, title, price, description, isbn, image, no_of_pages, price_unit, publication_year, genre, created_at, updated_at, specialisation):
        self.title = title
        self.price = price
        self.description = description
        self.isbn = isbn
        self.image = image
        self.no_of_pages = no_of_pages
        self.price_unit = price_unit
        self.publication_year = publication_year
        self.genre = genre
        self.created_at = created_at
        self.updated_at = updated_at
