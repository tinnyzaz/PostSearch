# PostSearch - A simple Python application to search through your old
# Tweets and Threads Posts from downloaded archive files.
# Author: Tinda Zaszcek
# Link: https://github.com/tinnyzaz/PostSearch
# database.py

# Functions to connect to the sqlite3 database

import sqlite3
import os

import config as cfg
from debug import debug, error, verbose

def dbconnect():
    # Connect to the SQLite database
    try:
        conn = sqlite3.connect(cfg.dbname)
        debug("Connected to the database successfully.")
        c = conn.cursor()
        return conn, c
    except sqlite3.Error as e:
        error(f"Error connecting to database: {e}")
        exit(1)

