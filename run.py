from app import create_app, socketio

# Create the app instance
app = create_app()

# Run the app with Socket.IO
if __name__ == '__main__':
    socketio.run(app, debug=True)
