import os
import yaml
import logging
import logging.config
from flask import Flask
from dotenv import load_dotenv

from app.services import init_cluster
from app.mqtt import mqtt, initialize_mqtt



LOCK_FILE = '.registration.lock'
LOGGING_CONFIG_FILE = 'logging_config.yml'


def run_registration_mode():
    # Registration Mode (Initialization Mode)
    logger.info('Registration Mode Entered.')
    init_cluster()


def run_cluster_mode():
    pass


def initialize_dotenv():
    dotenv_path = '.env'

    # Create the .env file if it does not exist
    if not os.path.exists(dotenv_path):
        with open(dotenv_path, 'w') as f:
            f.write('')

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
    # initialize_mqtt(app)

    global logger
    logger = logging.getLogger('app')


    # Check for the existence of the lock file
    if not os.path.exists(LOCK_FILE):
        run_registration_mode()
    else:
        run_cluster_mode()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)