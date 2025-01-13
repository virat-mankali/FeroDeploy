# from flask import Blueprint, current_app, jsonify, request
# from flask_socketio import emit

# # Create the blueprint for driver-related routes
# driver_bp = Blueprint("driver_bp", __name__)
# socketio = None  # Placeholder for SocketIO instance

# @driver_bp.record
# def record_params(setup_state):
#     """
#     Capture the SocketIO instance passed from `__init__.py`.
#     """
#     global socketio

#     socketio = setup_state.options.get("socketio")

#     if socketio is None:
#         print("SocketIO not passed to Blueprint")

# # Route to handle location updates from the driver
# @driver_bp.route("/location", methods=["POST"])
# def update_location():

#     global socketio

#     if socketio is None:
#         return jsonify({"error": "SocketIO instance not initialized"}), 500
    
#     data = request.json
#     if not data or "lat" not in data or "lng" not in data:
#         return jsonify({"error": "Invalid data"}), 400

#     # Emit the location update to all connected clients
#     socketio.emit("broadcast_location", {"lat": data["lat"], "lng": data["lng"]}, broadcast=True)
#     return jsonify({"message": "Location broadcasted"}), 200
