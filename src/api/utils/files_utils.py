import os
from zipfile import ZipFile

project_root = os.getcwd()
downloads_folder = os.path.join(project_root, 'data/downloads')

def zip_files(directory_name, zip_file_name):
   print(zip_file_name)
   print(directory_name)
   # Create object of ZipFile
   with ZipFile(zip_file_name, 'w') as zip_object:
    # Traverse all files in directory
    for folder_name, sub_folders, file_names in os.walk(directory_name):
        for filename in file_names:
            # Create filepath of files in directory
            file_path = os.path.join(folder_name, filename)
            # Add files to zip file
            zip_object.write(file_path, os.path.basename(file_path))