from flask import Flask # importing flask
from app.extensions import db, migrate, jwt # importing the database and migrate instance
from app.controllers.auth.auth_controller import auth

# Creating an apppliction factory function
def create_app():
    app = Flask(__name__) # creating an instance
    
    app.config.from_object('config.Config') # CONFIGURING THE DATABASE
    
    db.init_app(app) # accesing the instance
    migrate.init_app(app, db) # accesing the migrate instance
    jwt.init_app(app) # accesing the jwt instance
    
    
    
    # registering models
    from app.models.author_model import Author
    from app.models.company_model import Company
    from app.models.book_model import Book
    
    #registering blueprints

    app.register_blueprint(auth)
    
    @app.route('/') # index route
    def index():
        return 'Hello'
    
    
    return app # returning the app instance
    
     