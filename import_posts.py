# PostSearch - A simple Python application to search through your old
# Twitter and Threads posts from downloaded archive files. 
# Author: Tinda Zaszcek
# Link: https://github.com/tinnyzaz/PostSearch 
# import_posts.py
# 
# This script will import the posts from a provided JSON file into the
# database. It can be run on its own or it will run the first time the
# app loads.

import os
import sqlite3
import ijson

import debug
import config as cfg
from database import DatabaseConnection

def import_posts(source="twitter"):
    source = source.lower()
    if source == "twitter":
        jsonfile = os.path.join(cfg.post_archive_download_path, cfg.tweet_path, cfg.jsonfile_tweets)
        # Before we do anything, let's make sure we have a JSON file to work with
        if not os.path.exists(jsonfile):
            debug.error(f"The file '{jsonfile}' does not exist.")
            exit(1)
        # OK let's mosey!
        # Connect to the database
        with DatabaseConnection() as db_conn:
            try:
                # Check if the 'posts' table exists
                db_conn.db.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{cfg.table_name}'")
                debug.msg(f"Checking if the '{cfg.table_name}' table exists...")
                if db_conn.db.fetchone():
                    # If the 'posts' table exists, ask if we should drop it
                    response = input(f"The '{cfg.table_name}' table already exists. Do you want to drop it? (yes/no): ")
                    if response.lower() == 'yes':
                        db_conn.db.execute(f"DROP TABLE {cfg.table_name}")
                        debug.msg(f"Dropped the '{cfg.table_name}' table successfully.")
                    else:
                        debug.verbose(f"The '{cfg.table_name}' table was not dropped.")

                # Check if the 'posts' table exists
                db_conn.db.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{cfg.table_name}'")
                if db_conn.db.fetchone() is None:
                    # If the '{cfg.table_name}' table doesn't exist, create it
                    db_conn.db.execute(f'''
                                CREATE TABLE {cfg.table_name} (
                                    id_str TEXT PRIMARY KEY,
                                    created_at TEXT,
                                    full_text TEXT,
                                    favorite_count INTEGER,
                                    in_reply_to_status_id_str TEXT,
                                    is_archived BOOLEAN DEFAULT False
                                )
                            ''')
                    debug.msg(f"Created the '{cfg.table_name}' table successfully.")

                # Check if the JSON file exists
                if not os.path.exists(f'{jsonfile}'):
                    debug.error(f"The file '{jsonfile}' does not exist.")
                else:
                    debug.msg(f"Processing {jsonfile}...")
                    # Open the JSON file in streaming mode with UTF-8 encoding
                    with open(f'{jsonfile}', 'r', encoding='utf-8') as file:
                        # Use ijson to parse the JSON file stream
                        objects = ijson.items(file, 'my_tweets.item')
                        debug.msg(f"Processing {file}...")
                        new_posts = 0  # Initialize the counter

                        for i, post in enumerate(objects):
                            debug.verbose(f"Processing post {i}")
                            # Check if the required keys are in the post object
                            if 'id_str' in post['tweet'] and 'created_at' in post['tweet'] and 'full_text' in post['tweet'] and 'favorite_count' in post['tweet']:
                                # Extract the fields from the post object
                                id_str = post['tweet']['id_str']
                                created_at = post['tweet']['created_at']
                                full_text = post['tweet']['full_text']
                                favorite_count = int(post['tweet']['favorite_count'])
                                in_reply_to_status_id_str = post.get('in_reply_to_status_id_str', None)
                                # Set the is_archived flag to 0
                                is_archived = False
                                debug.msg(f"Processing post with ID: {id_str}...")
                                try:
                                    # Insert each object into the database
                                    db_conn.db.execute(f'''
                                        INSERT INTO {cfg.table_name} VALUES (?, ?, ?, ?, ?, ?)
                                    ''', (id_str, created_at, full_text, favorite_count, in_reply_to_status_id_str, is_archived))
                                    new_posts += 1  # Increment the counter
                                except sqlite3.IntegrityError:
                                    debug.warning(f"A post with ID {id_str} already exists. Skipping.")
                                    # Continue to the next post
                                    continue
                                except sqlite3.Error as e:
                                    debug.warning(f"{e.args[0]}. Skipping.")
                                    # Continue to the next post
                                    continue
                            else:
                                debug.error("One or more required keys are missing from the post object.")  # Shouldn't need to ever see this error
                                # pause for a moment to see if we can see the error
                                import time
                                time.sleep(5)


                            # Commit the transaction every 1000 posts
                            if i % 1000 == 0:
                                db_conn.conn.commit()
                                debug.info(f"Processed {i} posts...")
                        # Commit any remaining changes
                        db_conn.conn.commit()
                        debug.info(f"Found {new_posts} new posts.")
                        # Rudimentary check to see if the import was successful
                        db_conn.db.execute(f"SELECT COUNT(*) FROM {cfg.table_name}")
                        count = db_conn.db.fetchone()[0]
                        # Print the number of posts imported, and if they match we're gonna call that a win.
                        debug.info(f"Imported {count} posts successfully to {cfg.dbname}. Probably.")
            except Exception as e:
                debug.error(f"An error occurred while processing the JSON file: {e}")
            finally:
                    # Close the connection
                    db_conn.conn.close()
                    debug.msg("post import script completed. Great job!")
    elif source == "threads":
        pass
    else:
        debug.error("Invalid source specified. Please specify a valid source.")
        exit(1)

# Connect to database using existing connection method from database.py
# def connect_to_db():
#     with DatabaseConnection() as db_conn:
#         return db_conn
    
# # a function to check if a given file exists
# def check_file(file):
#     if not os.path.exists(file):
#         debug.msg(f"The file '{file}' does not exist.")
#         return False
#     else:
#         return True

# Check if the database table exists. If not, create it.
# def check_table():
#     with DatabaseConnection() as db_conn:
#         db_conn.db.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{cfg.table_name}'")
#         if db_conn.db.fetchone() is None:
#             db_conn.db.execute(f'''
#                         CREATE TABLE {cfg.table_name} (
#                             id_str TEXT PRIMARY KEY,
#                             created_at TEXT,
#                             full_text TEXT,
#                             favorite_count INTEGER,
#                             in_reply_to_status_id_str TEXT,
#                             is_archived BOOLEAN DEFAULT False
#                         )
#                     ''')
#             debug.msg(f"Created the '{cfg.table_name}' table successfully.")
#         else:
#             debug.msg(f"The '{cfg.table_name}' table already exists.")

# # Process the JSON file and import the posts
# def process_json(jsonfile):
#     # Check if the JSON file exists
#     if not check_file(jsonfile):
#         debug.error(f"The file '{jsonfile}' does not exist.")
#         exit(1)
#     # Open the JSON file in streaming mode with UTF-8 encoding
#     with open(jsonfile, 'r', encoding='utf-8') as file:
#         # Use ijson to parse the JSON file stream
#         objects = ijson.items(file, 'my_tweets.item')

#         new_posts = 0  # Initialize the counter
#         debug.msg(f"Processing {jsonfile}...")
#         for i, post in enumerate(objects):
#             # Check if the required keys are in the post object
#             if 'id_str' in post and 'created_at' in post and 'full_text' in post and 'favorite_count' in post:
#                 # Extract the fields from the post object
#                 id_str = post['id_str']
#                 created_at = post['created_at']
#                 full_text = post['full_text']
#                 favorite_count = int(post['favorite_count'])
#                 in_reply_to_status_id_str = post.get('in_reply_to_status_id_str', None)
#                 # Set the is_archived flag to 0
#                 is_archived = False
#                 debug.msg(f"Processing post with ID: {id_str}...")
#                 try:
#                     # Insert each object into the database
#                     db_conn.db.execute(f'''
#                         INSERT INTO {cfg.table_name} VALUES (?, ?, ?, ?, ?, ?)
#                     ''', (id_str, created_at, full_text, favorite_count, in_reply_to_status_id_str, is_archived))
#                     new_posts += 1  # Increment the counter
#                 except sqlite3.IntegrityError:
#                     debug.error(f"A post with ID {id_str} already exists. Skipping.")
#                     # Continue to the next post
#                     continue
#                 except sqlite3.Error as e:
#                     debug.error(f"{e.args[0]}. Skipping.")
#                     # Continue to the next post
#                     continue
#             else:
#                 debug.error("One or more required keys are missing from the post object.")  # Shouldn't need to ever see this error

#             # Commit the transaction every 1000 posts
#             if i % 1000 == 0:
#                 db_conn.conn.commit()
#                 debug.info(f"Processed {i} posts...")
#         # Commit any remaining changes
#         db_conn.conn.commit()

# A function to import a ZIP file and find the correct posts.txt file to import
# TODO: Implement this function
def import_zip(zipfile):
    # Import the required modules
    import zipfile
    import re

    # Open the ZIP file
    with zipfile.ZipFile(zipfile, 'r') as zip:
        # Get a list of all files in the ZIP file
        files = zip.namelist()
        # Search for the posts file
        for file in files:
            if re.match(r'^tweets.js$', file):
                # Extract the tweets.js file
                zip.extract(file)
                # Set the JSON file to the extracted file
                jsonfile = file
                # Run the import_posts function
                import_posts()
                # Exit the function
                return
        # If the tweets.js file is not found, print an error message
        debug.error("The tweets.js file was not found in the ZIP file.")
        # Exit the function
        return
    
if __name__ == '__main__':
    import_posts()