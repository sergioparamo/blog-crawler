from src.api.tasks.tasks import crawl_task
from src.api.utils.socketio_utils import socketio
import uuid

def start_crawl_process(data):
    request_id = str(uuid.uuid4())
    blog_url = data['blogUrl']
    years = data['years']
    populate_between = data.get('populateBetween', False)

    # Emit initial logs and progress
    socketio.emit('progress', {'progress': 5, 'requestId': request_id})
    socketio.emit('log', {'log': f"Starting crawl for {blog_url}", 'requestId': request_id})

    # Start Celery task
    task = crawl_task.apply_async(args=[blog_url, years, populate_between, {'request_id': request_id}])

    return {
        'status': 'started',
        'requestId': request_id,
        'taskId': task.id
    }
