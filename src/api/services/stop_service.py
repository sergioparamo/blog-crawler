from src.api.tasks.tasks import crawl_task
from src.api.utils.socketio_utils import socketio
from src.api.utils.context.context import request_id_var

def stop_process(task_id):
    task = crawl_task.AsyncResult(task_id)
    if task.state in ['PENDING', 'STARTED']:
        task.revoke(terminate=True)
        socketio.emit('state', {'state': "stopped", 'requestId': request_id_var.get()})
        return {'message': f'Task {task_id} revoked successfully'}, 200
    elif task.state == 'REVOKED':
        return {'message': f'Task {task_id} is already revoked'}, 400
    else:
        return {'message': f'Task {task_id} cannot be revoked in its current state: {task.state}'}, 400