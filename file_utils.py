import pandas as pd
import configparser
import os

class FileUtils:
    def __init__(self):
        pass
    
    def create_output_directory(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
            
    def read_input_file(self, input_file):
        config = configparser.ConfigParser()
        config.read(input_file)
        return config