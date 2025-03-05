# Storing functions used to perform differnt authentication process
# Controller functions are used to handle requests and return responses to the client
# Controller functions are defined as route handlers in Flask applications. They handle incoming requests

from flask import Blueprint, request, jsonify # Importing the Blueprint and request and jsonify classes from the flask module
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR,   HTTP_201_CREATED, HTTP_200_OK , HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT  # Importing the HTTP status codes from the status_codes module
import validators  # Importing the validators module
from app.models.author_model import Author  # Importing the Author model from the author_model module
from app.extensions import db, bcrypt  # Importing the db object from the extensions module
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity # Importing the create_access_token, create_refresh_token, jwt_required, and get_jwt_identity functions from the flask_jwt_extended module



auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')  # Creating a Blueprint instance
# 'auth'  is the name of the blueprint. It is used internally by Flask to identify the blueprint
# URL path prefix is used in web applications to define a base path for authentication-related API endpoints
# url_prefix='api/v1/auth - This sets a URL prefix for all the routes defined in this blueprint. 
# For example, if you define a route /login within this blueprint, it will be accessible at /api/v1/auth/login.


# User registration 
@auth.route('/register', methods=['POST'])  # Defining a route for user registration
# The route() decorator is used to bind a function to a URL 
# register is the url name
# The POST method is used to send data to the server to create/update a resource.

def register_user():
    data = request.json  # Extracting the JSON data as content type the request
    id = data.get('id')  # Extracting the id from the JSON data
    first_name = data.get('first_name')  
    last_name = data.get('last_name')  
    contact = data.get('contact')
    email = data.get('email')
    password = data.get('password')
    biography = data.get('biography', '')
    specialisation = data.get('specialisation', '')
    created_at = data.get('created_at', '')
    updated_at = data.get('updated_at', '')

    # Validations of incoming request 
    if not first_name or not last_name or not contact or not email or not password: # Checking if all required fields are filled
        return jsonify({'error': 'All fields are required'}), HTTP_400_BAD_REQUEST
    
    
    if type == 'author' and not biography:
        return jsonify({'error': 'Biography is required for authors'}), HTTP_400_BAD_REQUEST
    
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), HTTP_400_BAD_REQUEST
    
    if not validators.email(email):
        return jsonify({'error': 'Invalid email address'}), HTTP_400_BAD_REQUEST
    
    if Author.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already in use'}), HTTP_409_CONFLICT
    
    if Author.query.filter_by(contact=contact).first():
        return jsonify({'error': 'Contact already in use'}), HTTP_409_CONFLICT
    
    
    # the try block is used to handle potential exceptions that might occur during the process of creating and saving a new Author object to the database. 
    # The try block ensures that any errors during the creation and saving of the Author object are gracefully handled, 
    # providing a clear error message to the client instead of causing the server to crash or return an unhandled exception.
    
    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') # Hashing the password
        # Creating a new Author instance 
        author_1 = Author(id=id, first_name=first_name, last_name=last_name, contact=contact, email=email, password=hashed_password, biography=biography, specialisation = specialisation, created_at = created_at, updated_at = updated_at)    
        db.session.add(author_1)  # Adding the new Author instance to the database session
        db.session.commit()  # Committing the changes to the database   
        
        username = author_1.first_name + ' ' + author_1.last_name
        return jsonify({
            'message': username + ' has been registered successfully'}), HTTP_201_CREATED
    
    except Exception as e:
        db.session.rollback() # This line rolls back the current transaction in the database session
        # The rollback() method is used to undo all the changes made in the current transaction
        # If an error occurs (caught by the except block), 
        # db.session.rollback() is called to undo any changes made during the transaction.
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR # If an error occurs, a 500 Internal Server Error response is returned to the client
        
        
# User login        

@auth.route('/login', methods=['POST'])  # Defining a route for user login
def login():
    
    email = request.json.get('email')  # Extracting the email from the JSON data
    password = request.json.get('password')  # Extracting the password from the JSON data   
    
    
    try:
        
        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), HTTP_400_BAD_REQUEST
    
        author = Author.query.filter_by(email=email).first()  # Querying the Author table to find the user with the specified email
        
        if author:
            is_correct_password = bcrypt.check_password_hash(author.password, password)
        
            if is_correct_password: 
                access_token = create_access_token(identity=author.id)  # Creating an access token for the user
                refresh_token = create_refresh_token(identity=author.id)  # Creating a refresh token for the user




                return jsonify({
                    'message': 'You have successfully logged into your account',
                    'access_token': access_token,
                    'refresh_token': refresh_token
                    }), HTTP_200_OK
                
            else:
                return jsonify({'message': 'Invalid password'}), HTTP_401_UNAUTHORIZED

        else:
            return jsonify({'message': 'Invalid email address'}), HTTP_401_UNAUTHORIZED
    

    
    
    except Exception as e:
        return jsonify({
            'error': str(e)
            }), HTTP_500_INTERNAL_SERVER_ERROR
        
# Refresh token
@auth.route("/token/refresh", methods=["POST"])
@jwt_required(refresh=True) # This decorator is used to protect routes that require a valid refresh token
def refresh():
    identity = get_jwt_identity()  # Extracting the identity from the JWT token
    access_token = create_access_token(identity=identity) # Creating a new access token
    return jsonify({'access_token': access_token}), HTTP_200_OK
    
    
    
    
    