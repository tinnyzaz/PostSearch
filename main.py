# PostSearch - A simple Python application to search through your old
# Twitter and Threads posts from downloaded archive files.
# Author: Tinda Zaszcek
# Link: https://github.com/tinnyzaz/PostSearch
# main.py

import debug

from app_state import state
from gui import GUI
from database import DatabaseConnection
from utils.shortcuts import try_this

def main():
    # Loading user preferences
    try_this(state.load_user_config)
    debug.msg("Starting the main script...")
    # Connect to the database
    # try:        
    with DatabaseConnection() as db_conn:
        # Start the GUI script 
        debug.info("Starting the GUI...")
        GUI(db_conn)
        debug.info("Closing GUI...")
        # Commit changes
        db_conn.conn.commit()
    # except Exception as e:
    #     debug.error(f"101-An error occurred: {e}")
    # else:
        debug.msg("Main script completed. Great job!")

# ==============================================================================
# if state.DEBUGGING:
#     try:
#         import utils.temp_debug_funcs
#     except Exception as e:
#         debug.error(f"An error occurred: {e}")
#     else:
#         debug.msg("Temporary debug functions completed. Great job!")
# ==============================================================================

if __name__ == "__main__":
    main()
    exit(0)