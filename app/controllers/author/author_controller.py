from flask import Blueprint, request, jsonify # Importing the Blueprint and request and jsonify classes from the flask module
from app.status_codes import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK,HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED  # Importing the HTTP status codes from the status_codes module
from app.models.author_model import Author  # Importing the Author class from the author_model module
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity # Importing functions from the flask_jwt_extended module
from app.extensions import db, bcrypt  # Importing the db object from the extensions module

# Creating a Blueprint instance
author = Blueprint('author', __name__, url_prefix='/api/v1/auth')  


# Getting all authors from the database
@author.get('/authors')  
def get_all_authors():
    
    try:
        
        all_authors = Author.query.all() # Querying the database for all authors
        
        authors_data = [] # Creating an empty list to store the authors data
        for author in all_authors:
            author_info = {
                'id' : author.id,
                'first_name' : author.first_name,
                'last_name' : author.last_name,
                'email' : author.email,
                'contact' : author.contact,
                'biography' : author.biography,
                'specialisation' : author.specialisation,
                'created_at' : author.created_at
                
            } # Creating a dictionary to store the author's data
            authors_data.append(author_info) # Appending the author's data to the authors_data list
        
        return jsonify({
            'message': 'Authors retrieved successfully',
            'authors': authors_data
        }) , HTTP_200_OK # Returning a response to the client
    

    except Exception as e:
        return jsonify({
            'error': str(e)
            }), HTTP_500_INTERNAL_SERVER_ERROR
        


@author.get('/author/<int:id>')  
@jwt_required()
def get_author(id):
    
    try:
        
        author = Author.query.get(id) # Querying the database for the author with the specified id
       
        return jsonify({
            'message': 'Author retrieved successfully',
            'author': {
                'id' : author.id,
                'first_name' : author.first_name,
                'last_name' : author.last_name,
                'email' : author.email,
                'contact' : author.contact,
                'biography' : author.biography,
                'specialisation' : author.specialisation,
                'created_at' : author.created_at
            }
        }) , HTTP_200_OK 

    except Exception as e:
        return jsonify({
            'error': str(e)
            }), HTTP_500_INTERNAL_SERVER_ERROR
        
        
    
@author.route('/edit/<int:id>', methods=['PUT', 'PATCH']) # Defining a route for editing an author  
@jwt_required()
def update_author_details(id):
    
    try:
        
        current_author = get_jwt_identity() # Getting the current author's id from the access token
        logged_in_author = Author.query.filter_by(id=current_author).first() # Querying the database for the author with the specified id
        
        
        author = Author.query.get(id) # Querying the database for the author with the specified id
    
        
        
        if not author:
            return jsonify({'message': 'Author does not exist'}), HTTP_404_NOT_FOUND
        
        elif logged_in_author.id != author.id:
            return jsonify({'message': 'You are not authorized to edit this author'}), HTTP_401_UNAUTHORIZED
        
        else:
            data = request.get_json() # Extracting the JSON data
            first_name = data.get('first_name', author.first_name) # Extracting the first name from the JSON data
            last_name = data.get('last_name', author.last_name) # Extracting the last name from the JSON data
            contact = data.get('contact', author.contact)
            email = data.get('email', author.email)
            biography = data.get('biography', author.biography)
            specialisation = data.get('specialisation', author.specialisation)
            
            if "password" in request.json:
                password = request.json.get('password')
                hashed_password = bcrypt.generate_password_hash(password)
                author.password = hashed_password

            author.first_name = first_name
            author.last_name = last_name
            author.contact = contact
            author.email = email
            author.biography = biography
            author.specialisation = specialisation
            
            db.session.commit() # Committing the changes to the database
            
            author_name = author.first_name + ' ' + author.last_name
            return jsonify({
                'message': author_name + ' has been updated successfully',
                'author': {
                    'first_name' : author.first_name,
                    'last_name' : author.last_name,
                    'email' : author.email,
                    'contact' : author.contact,
                    'biography' : author.biography,
                    'specialisation' : author.specialisation,
                    'created_at' : author.created_at}
                }), HTTP_200_OK
            
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR













