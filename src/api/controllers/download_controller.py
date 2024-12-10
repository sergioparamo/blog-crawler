from flask import Blueprint, jsonify, send_file
from src.api.services.download_service import prepare_download

download_bp = Blueprint('download', __name__)

@download_bp.route('/api/download/<request_id>', methods=['GET'])
def download(request_id):
    file_path = prepare_download(request_id)
    
    if file_path:
        # Make sure to set the correct MIME type for ZIP files
        return send_file(file_path, 
                         as_attachment=True, 
                         download_name="blog_data.zip",  # File name for download
                         mimetype='application/zip')
    
    return jsonify({'error': 'File not found'}), 404