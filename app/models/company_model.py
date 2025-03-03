from app.extensions import db
from datetime import datetime

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    origin = db.Column(db.String(100))
    description = db.Column(db.String(100))
    created_at = db.Column(db.DateTime,  default = datetime.now())
    updated_at = db.Column(db.DateTime,  onupdate = datetime.now())
    specialisation = db.Column(db.String(50))
    
    
    def __init__(self, id, name, origin, description, created_at, updated_at, specialisation):
        self.id = id
        self.name = name
        self.origin = origin
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at


