import os
import yaml
import logging
import logging.config
from flask import Flask
from dotenv import load_dotenv

from app.services.registration_service import init_cluster

LOCK_FILE = '.registration.lock'
LOGGING_CONFIG_FILE = 'logging_config.yml'

logger = logging.getLogger('app')

def run_registration_mode():
    # Registration Mode (Initialization Mode)
    logger.info('Registration Mode Entered.')
    init_cluster(LOCK_FILE)


def run_cluster_mode():
    logger.info('Cluster Mode Entered.')
    # cluster_service





def initialize_dotenv():
    dotenv_path = '.env'

    # Create the .env file if it does not exist
    if not os.path.exists(dotenv_path):
        with open(dotenv_path, 'w') as f:
            pass

def initialize_logging():
    # Load logging configuration
    with open(LOGGING_CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)


def create_app():
    app = Flask(__name__)

    initialize_dotenv()
    load_dotenv()
    initialize_logging()

    # Check for the existence of the lock file
    if not os.path.exists(LOCK_FILE):
        run_registration_mode()
    else:
        from app.utils.mqtt.mqtt import initialize_mqtt
        mqtt = initialize_mqtt(app)
        run_cluster_mode()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)