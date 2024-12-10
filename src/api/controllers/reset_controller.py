from flask import Blueprint, jsonify
from src.api.services.reset_service import reset_process

reset_bp = Blueprint('reset', __name__)

@reset_bp.route('/api/reset/<request_id>', methods=['POST'])
def reset(request_id):
    reset_process(request_id)
    return jsonify({'status': 'success'})
