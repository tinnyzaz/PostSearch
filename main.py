# PostSearch - A simple Python application to search through your old
# Tweets and Threads Posts from downloaded archive files.
# Author: Tinda Zaszcek
# Link: https://github.com/tinnyzaz/PostSearch
# main.py

import sqlite3

import debug
import config as cfg

from gui import GUI
from database import DatabaseConnection
from funcs import check_first_run

def main():
    # Check to see if this is the first time the app has run
    check_first_run()
    debug.msg("Starting the main script...")
    # Connect to the database
    try:
        conn = sqlite3.connect(cfg.dbname)
        db = conn.cursor()
        db_conn = DatabaseConnection(conn, db)
        # Start the GUI script 
        debug.info("Starting the GUI...")
        gui = GUI(db_conn)
        debug.info("Closing GUI...")
        # Commit changes
        conn.commit()
    except Exception as e:
        debug.error(f"An error occurred: {e}")
    else:
        debug.msg("Main script completed. Great job!")

# ==============================================================================
if cfg.DEBUGGING:
    try:
        import utils.temp_debug_funcs
    except Exception as e:
        debug.error(f"An error occurred: {e}")
    else:
        debug.msg("Temporary debug functions completed. Great job!")
# ==============================================================================

if __name__ == "__main__":
    main()
    exit(0)