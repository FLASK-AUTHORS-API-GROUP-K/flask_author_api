from app.extensions import db
from datetime import datetime


class Author(db.Model):
    __tablename__ = "Authors"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.Integer, nullable=False, unique=True)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime,  default = datetime.now())
    updated_at = db.Column(db.DateTime,  onupdate = datetime.now())
    specialisation = db.Column(db.String(50))
    biography = db.Column(db.Text, nullable=True)

    #foreign keys
    book_id= db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    
    # Relationship to Book
    books = db.relationship('Book', back_populates='author')
    
    def __init__(self, id, first_name, last_name, contact, email, password, image, created_at, updated_at, biography, specialisation):
        self.first_name = first_name
        self.last_name = last_name
        self.contact = contact
        self.email = email
        self.password = password
        self.image = image
        self.created_at = created_at
        self.updated_at = updated_at
        self.biography = biography
        self.specialisation = specialisation
    
