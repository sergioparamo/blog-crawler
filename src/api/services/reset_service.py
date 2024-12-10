import os
from src.api.utils.files_utils import downloads_folder

def reset_process(request_id):
    user_filepath = os.path.join(downloads_folder, request_id + "_blog_data.zip")
    if os.path.exists(user_filepath):
        #remove file
        os.remove(user_filepath)
