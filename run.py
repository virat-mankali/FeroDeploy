import os
from app import create_app, socketio

# Create the app instance
app = create_app()

# Run the app with Socket.IO
if __name__ == '__main__':
    # Get the PORT from environment variables (default to 5000 if not set)
    port = int(os.environ.get("PORT", 5000))
    # Bind to all interfaces (0.0.0.0) and use the port
    socketio.run(app, host="0.0.0.0", port=port, debug=True)
