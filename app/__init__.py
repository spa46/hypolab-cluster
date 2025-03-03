import logging
import logging.config
from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os
import yaml

from app.utils.initial_request_utils import register_device
from app.utils.kafka_utils.producer import get_kafka_producer
from app.utils.kafka_utils.consumer import get_kafka_consumer

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

    # Initialize Kafka producer and consumer
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    auto_offset_reset = os.getenv("KAFKA_AUTO_OFFSET_RESET", "earliest")
    topic = os.getenv("KAFKA_TOPIC", "mytopic/init-cluster")

    # Check for the existence of the lock file
    if not os.path.exists(LOCK_FILE):
        # Registration Mode (Initialization Mode)
        from .routes import registration_bp
        app.register_blueprint(registration_bp)

        logger.info('Registration Mode Entered.')

        register_device()

        producer = get_kafka_producer(bootstrap_servers)
        consumer = get_kafka_consumer(bootstrap_servers, auto_offset_reset, topic)

        return app
    else:
        # Cluster Mode
        from .routes import cluster_bp
        app.register_blueprint(cluster_bp)

        logger.info('Cluster Mode Entered.')

        producer = get_kafka_producer(bootstrap_servers)
        consumer = get_kafka_consumer(bootstrap_servers, auto_offset_reset, topic)

        socketio.init_app(app)

        return app


if __name__ == '__main__':
    app, producer, consumer = create_app()
    if app:
        socketio.run(app, debug=True)