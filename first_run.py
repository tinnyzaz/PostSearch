# PostSearch - A simple Python application to search through your old
# Tweets and Threads Posts from downloaded archive files.
# Author: Tinda Zaszcek
# Link: https://github.com/tinnyzaz/PostSearch
# first_run.py
# 
# This is a script that will run when the user first startsthe
# application. We want to check and see if the user has the required
# files and directories to run the application. If they do not, we will
# create them for them.

import os
import zipfile
from pathlib import Path

import debug
import config as cfg

# Define the paths for the archive directory and the JS and JSON files
archive_dir = cfg.post_archive_download_path
js_file_path = cfg.archived_tweets_file
json_file_path = cfg.jsonfile_tweets

def find_archive_dir():
    # Check if the user has the required archive files
    if not os.path.exists(archive_dir):
        debug.first(f"Archive directory not found: {archive_dir}")
        # Create the directory
        try:
            os.makedirs(archive_dir)
            debug.first(f"Created archive directory: {archive_dir}")
        except Exception as e:
            debug.error(f"Error creating archive directory: {e}")
            return False
    return True

def find_archive_file():
    # Check if the user has the required archive files
    archive_file = "*.zip" # We only want to find ZIP files
    archive_files = list(Path(archive_dir).rglob(archive_file))
    try:
        if not archive_files:
            debug.first(f"Archive file not found: {archive_file}")
            # Prompt user to download their archive file
            debug.warning(f"Archive file not found: {archive_file}")
            debug.info(f"Please download your post archive ZIP file and place it in the '{archive_dir}' directory.")
            return False
        else:
            debug.first(f"Found archive file: {archive_files[0]}")
            return True
    except Exception as e:
        debug.error(f"Error finding archive file: {e}")
        return False

def extract_archive():
    # Extract the archive file
    archive_file = list(Path(archive_dir).rglob("*.zip"))[0]
    try:
        with zipfile.ZipFile(archive_file, "r") as zip_ref:
            zip_ref.extractall(archive_dir)
            debug.first(f"Extracted archive file: {archive_file}")
            return True
    except Exception as e:
        debug.error(f"Error extracting archive file: {e}")
        return False

def convert_js_to_json(js_file_path, json_file_path):
    with open(js_file_path, 'r') as file:
        data = file.read()

    start_index = data.index('[')
    json_data = '{"my_tweets":' + data[start_index:] + '}'

    with open(json_file_path, 'w') as file:
        file.write(json_data)

def run_first_time_setup():
    # List of setup tasks
    tasks = [find_archive_dir, find_archive_file, extract_archive]
    debug.first("Verifying archive path...")
    # Run each task
    for task in tasks:
        if not task():
            return

    convert_js_to_json(js_file_path, json_file_path)

    # create a .cfg file called first_run.cfg and write False
    # to it so that the first_run.py script will not run again
    try:    
        with open('first_run.cfg', 'w') as file:
            file.write("False")
    except Exception as e:
        debug.error(f"Error creating first_run.cfg file: {e}")
        exit(1)

# Run the setup when the module is run as a script
if __name__ == "__main__":
    run_first_time_setup()