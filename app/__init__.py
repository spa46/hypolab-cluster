from flask import Flask
from flask_socketio import SocketIO
from .utils.initial_request_utils import register_device

CONFIG_FILE = 'config.json'

socketio = SocketIO()

def create_app():
    app = Flask(__name__)

    # Initial request check and UUID handling
    register_device(CONFIG_FILE)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    socketio.init_app(app)

    return app

if __name__ == '__main__':
    app = create_app()
    if app:
        socketio.run(app, debug=True)