# PostSearch - A simple Python application to search through your old
# Tweets and Threads Posts from downloaded archive files.
# Author: Tinda Zaszcek
# Link: https://github.com/tinnyzaz/PostSearch
# main.py

from debug import debug, verbose, error, info
from gui import GUI
from database import dbconnect

debug("Starting the main script...")
# Connect to the database
conn, db = dbconnect()
# Start the GUI script 
info("Starting the GUI...")
gui = GUI(conn, db)
info("Closing GUI...")
# Commit changes and disconnect from the database
conn.commit()
conn.close()
debug("Closed the database connection successfully.")
debug("Main script completed. Great job!")
exit(0)