from flask import Blueprint, request, jsonify
from app.status_code import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
import validators
from app.models.author_model import Author
from app.extensions import db, bcrypt
from flask_jwt_extended import create_access_token, jwt_required,get_jwt_identity, create_refresh_token


auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

#user registration

@auth.route('/register', methods=['POST'])
def register_user():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact = data.get('contact')
    email = data.get('email')
    password = data.get('password')
    biography = data.get('biography')


    #validations of the incoming request

    if not first_name or not last_name or not contact or  not password or not email: #ensuring that not empty values are submitted
        return jsonify({"error":"All fields are required"}),HTTP_400_BAD_REQUEST
    
    if type  == 'author' and not biography:
        return jsonify({"error":"Enter your author biography"}),HTTP_400_BAD_REQUEST

    
    if len(password) < 8:
        return jsonify({"error":"Password is too short"}),HTTP_400_BAD_REQUEST #to ensure that the password is above 8 
    
    if not validators.email(email):
        return jsonify({"error":"Email is not valid"}),HTTP_400_BAD_REQUEST #to ensure that the email is valid
    
    if Author.query.filter_by(email=email).first() is not None:
        return jsonify({"error":"Email address already  in use"}),HTTP_409_CONFLICT  #to reject the already existig email
    
    if Author.query.filter_by(contact=contact).first() is not None:
        return jsonify({"error":"Contact already in use"}),HTTP_409_CONFLICT
    
    try:
       hashed_password = bcrypt.generate_password_hash(password) #hashing the password

       #creating a new author
       new_author = Author(
                       first_name=first_name,
                       last_name=last_name,
                       password=hashed_password,
                       email=email,
                       contact=contact,
                       biography=biography,
                       user_type=type
                       )
       db.session.add(new_author)  #to add the new instance 
       db.session.commit()

       #username
       username = new_author.get_full_name()

       return jsonify({
           'message':username + " has been successfully created as an " + new_author,
           'user':{
               'id':new_author.id,
               "first_name":new_author.first_name,
               "last_name":new_author.last_name,
               "email": new_author.email,
               "contact": new_author.contact,
               'biography':new_author.biography,
              'created_at':new_author.created_at,
           }
       }),HTTP_201_CREATED

    except Exception as e:   
        db.session.rollback() 
        return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    
    #author login
@auth.post('/login')
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    
    try:
       if not password or not email:
        return jsonify({'Message': "Email and Password are required."}), HTTP_400_BAD_REQUEST
    
    
       user = Author.query.filter_by(email=email).first()
       if user:
            is_correct_password = bcrypt.check_password_hash(user.password, password)
            if is_correct_password:
                   access_token = create_access_token(identity=user.id)
                   refresh_token = create_refresh_token(identity= user.id) 
                   return jsonify({
                'user':{
                    'id': user.id,
                    'username': user.get_full_name(),
                    'email': user.email,
                    'access_token': access_token,
                    'refresh_token': refresh_token, 
                    'type': user.user_type

                     },
                     'message': "You have successfully logged into your account."
                  }), HTTP_200_OK
            
            else: 
                return jsonify({'Message': "Invalid password."}), HTTP_401_UNAUTHORIZED
           

       else:
         return jsonify({'Message': "Invalid email address."}), HTTP_401_UNAUTHORIZED

    except Exception as e:
        return jsonify({
            'error': str(e)
            }), HTTP_500_INTERNAL_SERVER_ERROR


    
@auth.route("token/refresh", methods=["POST"])
@jwt_required(refresh=True) 
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)
