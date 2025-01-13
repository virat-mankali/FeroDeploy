from flask_jwt_extended import create_access_token, get_jwt_identity
from datetime import datetime, timedelta

def generate_token(user_id, role):
    if not isinstance(user_id, str):
        print(f"Converting user_id to string. Original type: {type(user_id)}")
        user_id = str(user_id)

    access_token = create_access_token(
        identity=user_id,  # Ensure this is a string
        additional_claims={"role": role},
        expires_delta=timedelta(days=1)
    )
    return access_token



def get_current_user():
    return get_jwt_identity()


# Function developed to enable Role based authorization
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if not claims or claims.get('role') != required_role:
                return jsonify({"message": "Access forbidden: Unauthorized role"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator



# Role required decorator: 

# from flask_jwt_extended import jwt_required, get_jwt_identity
# from functools import wraps
# from flask import jsonify

# def role_required(reqired_role):
#     def decorator(func):
#         @wraps(func)
#         @jwt_required() # Ensures the user is authenticated 
#         def wrapper(*args, **kwargs):

#             # Get the current user's identity from the JWT
#             current_user = get_jwt_identity()

#             # Check if the user's role matches the required role
#             if current_user['role'] != reqired_role:
#                 return jsonify({"message": "Access forbidden: You don't have the required role"}), 403
            
#             # If role matches, proceed with the request 
#             return func(*args, **kwargs)
        
#         return wrapper
    
#     return decorator