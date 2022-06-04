from flask import Blueprint, request
from flask.json import jsonify
from src.db import db2
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flasgger import swag_from
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_404_NOT_FOUND


authRoutes = Blueprint("authRoutes", __name__, url_prefix="/auth")

@authRoutes.route('/register', methods=['POST'])
@swag_from('./docs/auth/register.yaml')
def create_user():
    if request.method == "POST":

        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        email = request.json["email"]
        password = request.json["password"]

        user = db2.find_one({'email': email})
        if user:
            return jsonify({
                'error': 'User already exists'
            }), HTTP_409_CONFLICT


        pwd_hash = generate_password_hash(password)
        
        res = db2.insert_one({"first_name":first_name, "last_name":last_name, "email":email, "password":pwd_hash})
       
        return jsonify({
        'message': "User created",
        'user': email

    }), HTTP_201_CREATED


@authRoutes.route('/login',methods=["POST"])
@swag_from('./docs/auth/login.yaml')
def login():

    email = request.json["email"]
    password = request.json["password"]

    login_details = request.get_json() 

    user = db2.find_one({'email': login_details['email']})
    if not user:
        return jsonify({'message': 'User does not exist!'}), HTTP_404_NOT_FOUND

    if user:
        is_pass_correct = check_password_hash(user['password'], password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=user['email'])
            access_token = create_access_token(identity=user['email']) # create jwt token
    
            return jsonify({
                        'message': 'Success',
                        'user': {
                            'email': email,
                            'refresh': refresh,
                            'access': access_token,
                        }

                    }), HTTP_200_OK

    return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED

 
    
@authRoutes.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access': access
    }), HTTP_200_OK