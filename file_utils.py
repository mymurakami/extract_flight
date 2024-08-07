import pandas as pd
import configparser
import os

class FileUtils:
    def __init__(self):
        pass
    
    def folder_exists(self, folder_path):
        return os.path.isdir(folder_path)
    
    def get_latest_file(self, folder_path, pattern):
        # List all files in the directory
        files = os.listdir(folder_path)
    
        # Filter files that start with pattern and are not directories
        files = [f for f in files if f.startswith(pattern) and os.path.isfile(os.path.join(folder_path, f))]
    
        # Get the full path of the files
        full_paths = [os.path.join(folder_path, f) for f in files]
    
        # Find the file with the latest modification time
        if full_paths:
            latest_file = max(full_paths, key=os.path.getmtime)
            return latest_file
        else:
            return None

    def create_output_directory(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
            
    def read_input_file(self, input_file):
        config = configparser.ConfigParser()
        config.read(input_file)
        return config
        