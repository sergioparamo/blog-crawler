# socketio_handlers.py
from flask_socketio import SocketIO

# Crear la instancia de SocketIO
socketio = SocketIO(cors_allowed_origins="*", logger=True, engineio_logger=True, manage_session=True, message_queue='amqp://user:password@localhost:5672/test')

def init_socketio(app):
    socketio.init_app(app, cors_allowed_origins="*", logger=True, engineio_logger=True, manage_session=True, message_queue='amqp://user:password@localhost:5672/test')
    return socketio

def get_socketio():
    return socketio

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('progress')
def handle_progress(data):
    print(f"Progress: {data['progress']}")

@socketio.on('log')
def handle_log(data):
    print(f"Log: {data['log']}")
    
@socketio.on('finished')
def handle_finished(data):
    print(f"Finished: {data['finished']}")