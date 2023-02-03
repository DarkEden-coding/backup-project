import os
import shutil
import time
from darkdisplay.notification import DisplayNotification

import psutil


# function that checks if a process is running
def check_process(process_name):
    for proc in psutil.process_iter():
        try:
            # convert process name to lower case and remove .exe from the end
            if process_name.lower() in proc.name().lower().replace(".exe", ""):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


# function that gets all keys from the processes dictionary and checks if they are running
def get_running_processes(processes):
    for key in processes:
        processes[key] = check_process(key)
    return processes


def copy_folder_contents(src, dest, ignore=None):
    if ignore is None:
        ignore = []
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isfile(s):
            if item.startswith(tuple(ignore)) or item.endswith(tuple(ignore)):
                print(f"ignoring {s}")
            else:
                print(f"coping {s} to {d}")
                shutil.copy(s, d)
        else:
            print(f"creating {d}")
            os.makedirs(d, exist_ok=True)
            copy_folder_contents(s, d, ignore)


def make_notification(message):
    DisplayNotification(message, window_size="250x50")


# dictionary of processes to monitor
processes = {"stormworks": False, "pycharm": False}
del_processes = {"stormworks": False, "pycharm": False}

# loop that runs the check_process function every 5 seconds
while True:
    processes = get_running_processes(processes)
    print(processes)
    # if the process is running then set the corresponding del_processes key to true
    if processes["stormworks"]:
        del_processes["stormworks"] = True
    # if the process is not running and the del_processes key is true then run the function
    if not processes["stormworks"] and del_processes["stormworks"]:
        print("backing up stormworks files...")
        # make_notification("Backing up stormworks files...")
        # move/update files from the stormworks folder to the backup folder using shutil
        for folder in ['microprocessors', 'vehicles']:
            src_folder = f"C:/Users/shana/AppData/Roaming/Stormworks/data/{folder}"
            dest_folder = f"O:/Nextcloud Sync/Backup/stormworks/{folder}"
            os.makedirs(dest_folder, exist_ok=True)
            copy_folder_contents(src_folder, dest_folder)

        for folder in ['saves']:
            src_folder = f"C:/Users/shana/AppData/Roaming/Stormworks/{folder}"
            dest_folder = f"O:/Nextcloud Sync/Backup/stormworks/{folder}"
            os.makedirs(dest_folder, exist_ok=True)
            copy_folder_contents(src_folder, dest_folder)
        # set the del_processes key to false so the function is not run again
        del_processes["stormworks"] = False
    # if pycharm is running then set the corresponding del_processes key to true
    if processes["pycharm"]:
        del_processes["pycharm"] = True
    # if the process is not running and the del_processes key is true then run the function
    if not processes["pycharm"] and del_processes["pycharm"]:
        # moves files from O:\Python Files to O:\Nextcloud Sync\Python Files, ignores files that start with .sync or
        # .owncloud, using copy_folder_contents
        print("backing up pycharm files...")
        # make_notification("Backing up pycharm files...")
        src_folder = "O:/Python Files/"
        dest_folder = "O:/Nextcloud Sync/Python Files"
        os.makedirs(dest_folder, exist_ok=True)
        copy_folder_contents(src_folder, dest_folder, ignore=[".sync", ".owncloud", ".ini"])
        # set the del_processes key to false so the function is not run again
        del_processes["pycharm"] = False
    time.sleep(.1)
