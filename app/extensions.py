from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine




engine = create_engine("sqlite:///example.db")  # Change this to your database URL




migrate = Migrate()
db = SQLAlchemy()
Session = sessionmaker(bind=engine)
session = Session() 