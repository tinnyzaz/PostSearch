# PostSearch - A simple Python application to search through your old
# Twitter and Threads posts from downloaded archive files.
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
from import_posts import import_posts
import config as cfg

# Define the paths for the archive directory and the JS and JSON files
archive_dir = cfg.post_archive_download_path

debug.first(f"TODO: Are we creating & populating the user.cfg file here?")

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
            exit(1)
    
    tweets_folder = os.path.join(archive_dir, cfg.tweet_path)
    threads_folder = os.path.join(archive_dir, cfg.threads_path)
    folders = [tweets_folder, threads_folder]
    
    # TODO: Check the directory for post archive folders
    # We're looking for the /twitter/data/ and 
    # /instagram/your_instagram_activity/threads directories
    # any folder we find that begins with "twitter" or "instagram"
    # will be considered a post archive folder. If there are more
    # than one, we will use the first one we find.
    for folder in folders:
        if not os.path.exists(folder):
            debug.first(f"Archive folder not found: {folder}.")
            # Create the directory
            try:
                os.makedirs(folder)
                debug.first(f"Created archive folder: {folder}")
            except Exception as e:
                debug.error(f"Error creating archive folder: {e}")
                exit(1)
    return

def find_archive_file():
    # Check if the user has the required archive files
    archive_file = "*.zip" # We only want to find ZIP files
    archive_files = list(Path(archive_dir).rglob(archive_file))
    try:
        if not archive_files:
            # look for JSON files instead
            debug.first(f"Archive ZIP not found: {archive_file}")
            if not list(Path(archive_dir).rglob(cfg.jsonfile_tweets)):
                debug.first(f"Archive JSON not found: {cfg.jsonfile_tweets}")                
                # Prompt user to download their archive file
                debug.warning(f"Please download your post archive ZIP file and place it in the '{archive_dir}' directory.")
                debug.warning(f"Or, unzip the archive yourself and place your '{cfg.archived_tweets_file}' file in the '{archive_dir}/{cfg.tweet_path}' directory.")
                return False
            else:
                # TODO: convert .js to .json if necessary
                pass
        else:
            debug.first(f"Found archive file: {archive_files[0]}")
            # extract the archive ZIP file
            pass
            return True
    except Exception as e:
        debug.error(f"Error finding archive file: {e}")
        return False

def extract_archive():
    # Extract the archive file
    debug.first(f"Extracting archive file if it exists...")
    try:
        archive_file = list(Path(archive_dir).rglob("*.zip"))[0]
        with zipfile.ZipFile(archive_file, "r") as zip_ref:
            zip_ref.extractall(archive_dir)
            debug.first(f"Extracted archive file: {archive_file}")
            return True
    except Exception as e:
        debug.error(f"Error extracting archive file: {e}")
        return False

def convert_js_to_json(js_file_path, json_file_path):
    debug.first(f"Converting {js_file_path} to {json_file_path} if necessary")
    try:
        with open(js_file_path, 'r') as file:
            data = file.read()
        start_index = data.index('[')
        json_data = '{\n\t"my_tweets":' + data[start_index:] + '}'
        with open(json_file_path, 'w') as file:
            file.write(json_data)
        debug.first(f"Converted {js_file_path} to {json_file_path}")
        return True
    except Exception as e:
        debug.error(f"Error converting {js_file_path} to {json_file_path}: {e}")
        return False

def run_first_time_setup():
    # List of setup tasks
    tasks = [find_archive_dir, find_archive_file, extract_archive]
    debug.first("Running setup tasks...")
    # Run each task
    for task in tasks:
        if not task():
            return

    try:
        # debug.msg("Converting tweets.js to tweets.json...SKIPPING")
        # convert_js_to_json(js_file_path, json_file_path) # we should do this elsewhere
        debug.first("Importing twitter posts...")
        import_posts("twitter")
    except Exception as e:
        debug.first(f"Error importing posts: {e}")
        return
    try:
        import_posts("threads")
    except Exception as e:
        debug.first(f"Importing threads not yet implemented.")
        return

    # create a .cfg file called first_run.cfg and write False
    # to it so that the first_run.py script will not run again
    # try:    
    #     debug.first("Creating first_run.cfg file...")
    #     with open('first_run.cfg', 'w') as file:
    #         file.write("False")
    # except Exception as e:
    #     debug.first(f"Error creating first_run.cfg file: {e}")
    #     return
    
    debug.first("Setup completed successfully.")
    # set FIRST_RUN to False in user.cfg
    try:
        # Open the file in write mode to overwrite existing content
        with open(cfg.user_cfg, "w") as file:  
            file.write(f"FIRST_RUN=FALSE\n")    # quick and dirty for now
            # eventually we want to write the entire user config here.
            debug.first(f"Updated {cfg.user_cfg}")
    except Exception as e:
        debug.error(f"Error saving {cfg.user_cfg}: {e}")

# Run the setup when the module is run as a script
if __name__ == "__main__":
    run_first_time_setup()