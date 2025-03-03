from flask import Blueprint, request, jsonify
from .services import register_hypo_cluster, get_hypo_cluster_status, control_hypo_cluster, monitor_hypo_cluster
import logging
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

registration_bp = Blueprint('init', __name__)

@registration_bp.route('/registration')
def registration():
    from .config import LOCK_FILE

    # Load environment variables from .env file
    load_dotenv()

    # Set Kafka values
    # os.environ["KAFKA_BROKER"] = "kafka-broker:9092"
    # os.environ["KAFKA_TOPIC"] = os.getenv('uuid')
    # os.environ["KAFKA_GROUP_ID"] = "my_group"
    #
    # # Create the lock file after registration
    # with open(LOCK_FILE, 'w') as f:
    #     f.write('')
    # logger.info('Device registered and lock file created.')

    # Print countdown and restart server
    for i in range(5, 0, -1):
        logger.info(f"Server restarting in {i} seconds...")
        time.sleep(1)

    os.execv(__file__, ['python'] + sys.argv)

    return 'Registration successful!'