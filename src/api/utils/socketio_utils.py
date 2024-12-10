from flask_socketio import SocketIO, disconnect
from src.api.utils.context.context import request_id_var
socketio = SocketIO(cors_allowed_origins="*", logger=True, engineio_logger=True, manage_session=True, message_queue='amqp://user:password@localhost:5672/test')

def init_socketio(app):
    socketio.init_app(app, cors_allowed_origins="*", logger=True, engineio_logger=True, manage_session=True, message_queue='amqp://user:password@localhost:5672/test')
    return socketio

def get_socketio():
    return socketio

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    # Assuming that 'requestId' is passed as a query parameter or through a header during connection
    # Set the requestId context variable when the client connects (you can retrieve it from the query parameter or header)
    request_id = request_id_var.get()  # Get the requestId if available
    if request_id:
        socketio.join_room(request_id)
        print(f"Client joined room: {request_id}")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('join_room')
def join_room(data):
    """Join the room based on the requestId sent from the client."""
    request_id = data.get('requestId')
    if request_id:
        socketio.join_room(request_id)  # Join the room
        print(f"Client joined room: {request_id}")

@socketio.on('leave_room')
def leave_room(data):
    """Leave the room when disconnecting or stopping."""
    request_id = data.get('requestId')
    if request_id:
        socketio.leave_room(request_id)  # Leave the room
        print(f"Client left room: {request_id}")

@socketio.on('progress')
def handle_progress(data):
    request_id = request_id_var.get()
    if request_id:
        # Emit to the room identified by requestId
        socketio.emit('progress', data, room=request_id)

@socketio.on('log')
def handle_log(data):
    request_id = request_id_var.get()
    if request_id:
        # Emit to the room identified by requestId
        socketio.emit('log', data, room=request_id)

@socketio.on('state')
def handle_state(data):
    request_id = request_id_var.get()
    if request_id:
        # Emit to the room identified by requestId
        socketio.emit('state', data, room=request_id)
        if data['state'] in ['failed', 'stopped']:
            disconnect()