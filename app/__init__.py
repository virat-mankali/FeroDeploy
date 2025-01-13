from flask import Flask 
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO, emit

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["mydatabase"]

# Initialize SocketIO globally
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)

    # Pass MongoDB Connection to Routes
    app.config['db'] = db

    # Configure JWT
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

    # Initialize JWT
    jwt = JWTManager(app)

    # Initialize CORS
    CORS(app)

    # Initialize SocketIO 
    socketio.init_app(app)

    # Register routes for user.py
    from app.routes.users import user_bp
    app.register_blueprint(user_bp, url_prefix="/auth")

    # Register routes for driver.py
    # from app.routes.driver import driver_bp
    # app.register_blueprint(driver_bp, url_prefix="/driver", options={"socketio": socketio})

    # Define SocketIO events here 
    @socketio.on("connect")
    def handle_connect():
        print("A client connected!")

    @socketio.on("location_update")
    def handle_location_update(data):
        print("Received location:", data)

        # Broadcast the location to all connected clients
        emit("broadcast_location", data, broadcast=True)

    return app