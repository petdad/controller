import os
import time
import logging
import requests
from dotenv import load_dotenv
from data_collector import read_data_from_file, write_data_to_file

load_dotenv()
CLOUD_SERVER_URL = os.getenv('CLOUD_SERVER_URL')
INTERVAL = int(os.getenv('INTERVAL', 60))
LOG_FILE_PATH = os.getenv('LOG_FILE_PATH', '/var/log/iot_controller.log')
DATA_FILE_PATH = os.getenv('DATA_FILE_PATH', 'data.txt')

logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def send_data_to_cloud(data):
    try:
        response = requests.post(CLOUD_SERVER_URL, json=data)
        response.raise_for_status()
        logging.info(f"Data sent successfully: {response.json()}")
    except requests.RequestException as e:
        logging.error(f"Failed to send data: {e}")

def get_data_from_cloud():
    try:
        response = requests.get(CLOUD_SERVER_URL)
        response.raise_for_status()
        data = response.json()
        logging.info(f"Data received: {data}")
        return data
    except requests.RequestException as e:
        logging.error(f"Failed to receive data: {e}")
        return None

def main():
    while True:
        data_to_send = read_data_from_file(DATA_FILE_PATH)
        
        if data_to_send:
            send_data_to_cloud(data_to_send)
        
        received_data = get_data_from_cloud()
        
        if received_data:
            logging.info(f"Processing received data: {received_data}")
            write_data_to_file(DATA_FILE_PATH, received_data)

        time.sleep(INTERVAL)

if __name__ == "__main__":
    if os.name == 'nt':
        import win32com.client
        import win32api
        import win32con
        import sys
        
        # Set the script to run at startup
        shell = win32com.client.Dispatch("WScript.Shell")
        startup_folder = shell.SpecialFolders("Startup")
        shortcut_path = os.path.join(startup_folder, "IoTController.lnk")
        
        if not os.path.exists(shortcut_path):
            shortcut = shell.CreateShortcut(shortcut_path)
            shortcut.TargetPath = sys.executable
            shortcut.WorkingDirectory = os.path.dirname(sys.executable)
            shortcut.save()

    main()
