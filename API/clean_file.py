import os
import schedule
import time
import threading

def clean_files(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return
    
    # List all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def schedule_clean_files(folder_path, interval):
    schedule.every(interval).seconds.do(clean_files, folder_path=folder_path)
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_cleaning_thread(folder_path, interval):
    cleaning_thread = threading.Thread(target=schedule_clean_files, args=(folder_path, interval))
    cleaning_thread.daemon = True  # Daemonize thread
    cleaning_thread.start()
    return cleaning_thread
