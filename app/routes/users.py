from flask import Blueprint, jsonify, current_app, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
import bcrypt
from app.utils.helpers import generate_token
from bson import ObjectId
from bson.errors import InvalidId

user_bp = Blueprint('user_bp', __name__)


# Create a new user 
@user_bp.route('/register', methods=['POST'])
def create_user():

    data = request.json

    if not data.get('name') or not data.get('email') or not data.get('phone') or not data.get('password') or not data.get('role'):
        return jsonify({"message": "All fields are required"}), 400
    
    # Hash the password 
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    # Insert the user into the database 
    new_user = {
        "name": data['name'],
        "email": data['email'],
        "phone": int(data['phone']),
        "password": hashed_password,
        "role": str(data['role'])
    }

    # Calling the MongoDB into the route
    db = current_app.config['db']
    users_collection = db['users']

    # Check if the user already exists
    if users_collection.find_one({"email": data['email']}):
        return jsonify({"message": "User already exists"}), 400
    
    # Insert the user into the database
    result = users_collection.insert_one(new_user)

    return jsonify({"message": "User created successfully", 'id': str(result.inserted_id)}), 201


# User login into app (Validate Password and JWT Generation)
@user_bp.route('/login', methods=['POST'])
def login_user():

    # Get the data from client side 
    data = request.json

    if not data.get('email') or not data.get('password'):
        return jsonify({"message": "Please identify using email and authenticate yourself using password!"}), 400
    
    # Access the MongoDB collection into the route
    db = current_app.config['db']
    users_collection = db['users']

    # Find the user in the database
    user = users_collection.find_one({"email": data['email']})

    if not user: 
        return jsonify({"message": "User not found"}), 404
    
    # Check if the password is correct 
    if not bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
        return jsonify({"message": "Invalid password"}), 401

    # Generate JWT token
    token = generate_token(user['_id'], user['role'])

    print("Token Payload:", {"_id": str(user['_id']), "role": user['role']})

    return jsonify({"message": "Login successful", "token": token, "role": user['role']}), 200


# Fetch all the users without passwords
@user_bp.route('/fetch', methods=['GET'])
@jwt_required()
def fetch_users():

    # Calling the MongoDB into the route
    db = current_app.config['db']
    users_collection = db['users']

    # Get the current user 
    current_user = get_jwt_identity()

    # fetch all the users without password 
    users = [
        {
            "id": str(user['_id']),
            "name": user['name'],
            "email": user['email'],
            "phone": user['phone']
        }
        for user in users_collection.find()
    ]

    return jsonify({"users": users, "current_user": current_user}), 200


@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    current_user_id = get_jwt_identity()  # Fetch the user ID directly
    current_user_id_converted_to_string = str(current_user_id)

    if not current_user_id:
        return jsonify({"message": "Invalid user identity"}), 400

    db = current_app.config['db']
    users_collection = db['users']

    try:
        user = users_collection.find_one({"_id": ObjectId(current_user_id)})
    except InvalidId:
        return jsonify({"message": "Invalid user ID format"}), 400

    if not user:
        return jsonify({"message": "User not found"}), 404
    
    print(f"Current User ID from JWT: {current_user_id} (type: {type(current_user_id)})")

    user_data = {
        "name": user['name'],
        "email": user['email'],
        "phone": str(user['phone'])
    }

    return jsonify(user_data), 200
