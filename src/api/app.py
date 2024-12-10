"""Blog Crawler API."""

import eventlet
eventlet.monkey_patch(all=False, socket=True)

from flask import Flask
from flask_cors import CORS
from src.api.utils.socketio_utils import init_socketio
from src.api.controllers.crawl_controller import crawl_bp
from src.api.controllers.reset_controller import reset_bp
from src.api.controllers.download_controller import download_bp

def create_socketio(app):
    socketio = init_socketio(app)
    return socketio

def create_app():
    """Factory function to create a Flask app."""
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Register Blueprints
    app.register_blueprint(crawl_bp)
    app.register_blueprint(reset_bp)
    app.register_blueprint(download_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    socketio = create_socketio(app)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)