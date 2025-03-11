import os
import  sys
import logging
import requests
from dotenv import load_dotenv

from app.utils import utils


logger = logging.getLogger(__name__)


def init_cluster(lock_file):
    load_dotenv()
    url = os.getenv('BACKEND_URL')
    topic = os.getenv('TOPIC')

    try:
        if not topic:
            response = requests.post(f'{url}/api/clusters/init-cluster/')
            logger.info("Registration request sent")
        else:
            response = requests.post(f'{url}/api/clusters/init-cluster/', json={'id': topic})
            logger.info("Registration already registered")

        if response.status_code == 200:
            logger.info("Registration Successful.")
            utils.save_to_dotenv('topic', response.json()['id'])
            # change_subscription(os.getenv('topic'))

            utils.create_lock_file(lock_file)
            logger.info('Device registered and lock file created.')

            utils.restart_server()
        else:
            logger.error(f"Registration request failed with status code: {response.status_code}")
            sys.exit(1)
    except requests.RequestException as e:
        logger.error(f"Registration failed with exception: {e}")
        sys.exit(1)

    # Create the lock file after registration

    return {'message': 'Hypo cluster registered successfully'}