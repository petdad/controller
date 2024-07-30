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


def write_data_to_file(file_path, data):
    with open(file_path, 'w') as file:
        for key, value in data.items():
            file.write(f'{key}={value}\n')