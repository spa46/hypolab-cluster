import logging
import logging.config
import yaml
from flask import Flask
from flask_socketio import SocketIO
from .utils.initial_request_utils import register_device
import os

CONFIG_FILE = 'config.yml'
LOCK_FILE = '.registration.lock'
LOGGING_CONFIG_FILE = 'logging_config.yml'

socketio = SocketIO()

def create_app():
    app = Flask(__name__)

    # Load logging configuration
    with open(LOGGING_CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)

    logger = logging.getLogger('app')

    # Check for the existence of the lock file
    if not os.path.exists(LOCK_FILE):
        register_device(CONFIG_FILE)
        # Create the lock file after registration
        with open(LOCK_FILE, 'w') as f:
            f.write('')
        logger.info('Device registered and lock file created.')
    else:
        logger.info('Cluster is already registered!')

    from .routes import main_bp
    app.register_blueprint(main_bp)

    socketio.init_app(app)

    return app

if __name__ == '__main__':
    app = create_app()
    if app:
        socketio.run(app, debug=True)