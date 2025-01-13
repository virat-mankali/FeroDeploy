# from flask_socketio import SocketIO, emit
# from flask_jwt_extended import decode_token
# from functools import wraps
# from flask import jsonify

# def role_required_socketio(required_role):
#     def decorator(event_handler):
#         @wraps(event_handler)
#         def wrapper(data):
#             # Extract JWT from the data payload
#             token = data.get("token")
#             if not token:
#                 return emit("error", {"message": "Missing authentication token"})

#             try:
#                 decoded_token = decode_token(token)
#                 if decoded_token["role"] != required_role:
#                     return emit("error", {"message": "Access forbidden: insufficient role"})
#             except Exception as e:
#                 return emit("error", {"message": "Invalid token"})

#             return event_handler(data)
#         return wrapper
#     return decorator

# def register_socketio_events(socketio):
#     @socketio.on("connect")
#     def handle_connect():
#         print("A client connected!")

#     @socketio.on("location_update")
#     @role_required_socketio("driver")
#     def handle_location_update(data):
#         print("Received location:", data)

#         # Broadcast the location to all connected clients
#         emit("broadcast_location", data, broadcast=True)
