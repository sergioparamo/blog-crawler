import os
from src.api.utils.files_utils import downloads_folder

def prepare_download(request_id):
    file_path = os.path.join(downloads_folder, request_id + "_blog_data.zip")
    if os.path.exists(file_path):
        return file_path
    return None
