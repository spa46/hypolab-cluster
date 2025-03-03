import logging
import logging.config
from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os
import yaml

from app.utils.initial_request_utils import register_device

LOCK_FILE = '.registration.lock'
LOGGING_CONFIG_FILE = 'logging_config.yml'

socketio = SocketIO()

def create_app():
    app = Flask(__name__)

    # Load environment variables from .env file
    load_dotenv()

    # Load logging configuration
    with open(LOGGING_CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)

    logger = logging.getLogger('app')

    # Check for the existence of the lock file
    if not os.path.exists(LOCK_FILE):
        # Registration Mode (Initialization Mode)
        from .routes import registration_bp
        app.register_blueprint(registration_bp)

        logger.info('Registration Mode Entered.')

        register_device()

        return app
    else:
        # Cluster Mode
        from .routes import cluster_bp
        app.register_blueprint(cluster_bp)

        logger.info('Cluster Mode Entered.')

        socketio.init_app(app)

        return app


if __name__ == '__main__':
    app = create_app()
    if app:
        socketio.run(app, debug=True)