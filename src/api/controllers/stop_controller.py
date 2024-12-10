from flask import Blueprint, jsonify
from src.api.services.stop_service import stop_process
from src.api.utils.socketio_utils import socketio
from src.api.utils.context.context import request_id_var
stop_bp = Blueprint('stop', __name__)

@stop_bp.route('/api/stop/<task_id>', methods=['POST'])
def reset(task_id):
    socketio.emit('log', {'log': f"Stopping process...", 'requestId': request_id_var.get()})
    response, status_code = stop_process(task_id)
    return jsonify(response), status_code
