# data.py
import os

def read_data_from_file(file_path):
    data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                key, value = line.strip().split('=')
                data[key] = value
    return data
