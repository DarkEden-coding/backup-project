## Backup Script
### Introduction
This is a Python script that checks if certain processes are running and if so, backs up files related to those processes. The processes being monitored are "Stormworks" and "Pycharm". If either of these processes is running, the script will copy files from specific folders to a backup folder. The backup process is indicated by a notification.

## Requirements
The script requires the following libraries to be installed:
```
os
shutil
time
psutil
darkdisplay
```

## How it works
The script defines a check_process function that takes the name of a process and returns a boolean indicating if the process is running or not.

It then defines a get_running_processes function that takes a dictionary of processes as an argument, uses the check_process function to check the status of each process, and updates the dictionary with the results.

The script then enters a loop that checks the status of the monitored processes every 1 second and backs up the relevant files if the process is no longer running.

The copy_folder_contents function is used to copy the files, and the make_notification function creates a notification to indicate the start of the backup process.

The script uses the shutil library to copy files and the psutil library to check if processes are running. The darkdisplay.notification library is used to display notifications.