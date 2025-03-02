from flask import Blueprint, request, jsonify
from .services import register_hypo_cluster, get_hypo_cluster_status, control_hypo_cluster, monitor_hypo_cluster
import logging

logger = logging.getLogger(__name__)

registration_bp = Blueprint('init', __name__)

@registration_bp.route('/registration')
def registration():
    from .config import LOCK_FILE

    # Create the lock file after registration
    with open(LOCK_FILE, 'w') as f:
        f.write('')
    logger.info('Device registered and lock file created.')
    return 'Registration successful!'


cluster_bp = Blueprint('main', __name__)

@cluster_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    response = register_hypo_cluster(data)
    return jsonify(response), 201

@cluster_bp.route('/status', methods=['GET'])
def status():
    response = get_hypo_cluster_status()
    return jsonify(response), 200

@cluster_bp.route('/control', methods=['PUT'])
def control():
    data = request.get_json()
    response = control_hypo_cluster(data)
    return jsonify(response), 200

@cluster_bp.route('/monitor', methods=['GET'])
def monitor():
    response = monitor_hypo_cluster()
    return jsonify(response), 200

