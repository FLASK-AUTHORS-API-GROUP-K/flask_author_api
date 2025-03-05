from flask import Flask
from app.extensions import db,migrate

def create_app():  #application factory function
    
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app) #intializing app extension
    migrate.init_app(app,db)
    
    
    #registering models 
    from app.models.author_model import Author
    from app.models.book_model import Book
    from app.models.company_model import Company
    
    #index route
    @app.route('/') 
    def index():
        return "World"


    return app #returning app instance
    
