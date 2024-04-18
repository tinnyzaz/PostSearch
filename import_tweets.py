import os
import sqlite3
import ijson

from debug import debug, verbose, error, info
import config as cfg
from database import dbconnect

def import_tweets():
    # Connect to the SQLite database
    conn, db = dbconnect()

    try:
        # Check if the 'tweets' table exists
        db.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{cfg.table_name}'")
        debug(f"Checking if the '{cfg.table_name}' table exists...")
        if db.fetchone():
            # If the 'tweets' table exists, ask if we should drop it
            response = input(f"The '{cfg.table_name}' table already exists. Do you want to drop it? (yes/no): ")
            if response.lower() == 'yes':
                db.execute(f"DROP TABLE {cfg.table_name}")
                debug(f"Dropped the '{cfg.table_name}' table successfully.")
            else:
                verbose(f"The '{cfg.table_name}' table was not dropped.")

        # Check if the 'tweets' table exists
        db.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{cfg.table_name}'")
        if db.fetchone() is None:
            # If the '{cfg.table_name}' table doesn't exist, create it
            db.execute(f'''
                        CREATE TABLE {cfg.table_name} (
                            id_str TEXT PRIMARY KEY,
                            created_at TEXT,
                            full_text TEXT,
                            favorite_count INTEGER,
                            in_reply_to_status_id_str TEXT,
                            is_archived BOOLEAN DEFAULT False
                        )
                    ''')
            debug(f"Created the '{cfg.table_name}' table successfully.")

        # Check if the JSON file exists
        if not os.path.exists(f'{cfg.jsonfile}'):
            error(f"The file '{cfg.jsonfile}' does not exist.")
        else:
            # Open the JSON file in streaming mode with UTF-8 encoding
            with open(f'{cfg.jsonfile}', 'r', encoding='utf-8') as file:
                # Use ijson to parse the JSON file stream
                objects = ijson.items(file, 'my_tweets.item.tweet') # TODO: This will need to be updated based on the JSON structure

                for i, tweet in enumerate(objects):
                    
                    # Check if the required keys are in the tweet object
                    if 'id_str' in tweet and 'created_at' in tweet and 'full_text' in tweet and 'favorite_count' in tweet:
                        # Extract the fields from the tweet object
                        id_str = tweet['id_str']
                        created_at = tweet['created_at']
                        full_text = tweet['full_text']
                        favorite_count = int(tweet['favorite_count'])
                        in_reply_to_status_id_str = tweet.get('in_reply_to_status_id_str', None)
                        # Set the is_archived flag to 0
                        is_archived = False
                        debug(f"Processing tweet with ID: {id_str}...")
                        try:
                            # Insert each object into the database
                            db.execute('''
                                INSERT INTO tweets VALUES (?, ?, ?, ?, ?, ?)
                            ''', (id_str, created_at, full_text, favorite_count, in_reply_to_status_id_str, is_archived))
                        except sqlite3.IntegrityError:
                            error(f"A tweet with ID {id_str} already exists. Skipping.")
                            # Continue to the next tweet
                            continue
                        except sqlite3.Error as e:
                            error(f"{e.args[0]}. Skipping.")
                            # Continue to the next tweet
                            continue
                    else:
                        error("One or more required keys are missing from the tweet object.") # Shouldn't need to ever see this error
                    
                    # Commit the transaction every 1000 tweets
                    if i % 1000 == 0:
                        conn.commit()

                # Commit any remaining changes
                conn.commit()
                info(f"Found {i+1} tweets.")
                # Rudimentary check to see if the import was successful
                db.execute(f"SELECT COUNT(*) FROM {cfg.table_name}")
                count = db.fetchone()[0]
                # Print the number of tweets imported, and if they match we're gonna call that a win.
                info(f"Imported {count} tweets successfully. Probably.")
    except Exception as e:
        error(f"An error occurred while processing the JSON file: {e}")
    finally:
            # Close the connection
            conn.close()
            debug("Tweet import script completed. Great job!")
            exit(1)

# A function to import a ZIP file and find the correct tweets.txt file to import
# TODO: Implement this function
def import_zip(zipfile):
    # Import the required modules
    import zipfile
    import re

    # Open the ZIP file
    with zipfile.ZipFile(zipfile, 'r') as zip:
        # Get a list of all files in the ZIP file
        files = zip.namelist()
        # Search for the tweets.txt file
        for file in files:
            if re.match(r'^tweets.txt$', file):
                # Extract the tweets.txt file
                zip.extract(file)
                # Set the JSON file to the extracted file
                cfg.jsonfile = file
                # Run the import_tweets function
                import_tweets()
                # Exit the function
                return
        # If the tweets.txt file is not found, print an error message
        error("The tweets.txt file was not found in the ZIP file.")
        # Exit the function
        return

# Run the import_tweets function
import_tweets()