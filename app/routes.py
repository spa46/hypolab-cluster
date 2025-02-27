from flask import Blueprint, request, jsonify
from .services import register_hypo_cluster, get_hypo_cluster_status, control_hypo_cluster, monitor_hypo_cluster

main_bp = Blueprint('main', __name__)

@main_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    response = register_hypo_cluster(data)
    return jsonify(response), 201

@main_bp.route('/status', methods=['GET'])
def status():
    response = get_hypo_cluster_status()
    return jsonify(response), 200

@main_bp.route('/control', methods=['PUT'])
def control():
    data = request.get_json()
    response = control_hypo_cluster(data)
    return jsonify(response), 200

@main_bp.route('/monitor', methods=['GET'])
def monitor():
    response = monitor_hypo_cluster()
    return jsonify(response), 200

