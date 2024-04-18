# PostSearch - A simple Python application to search through your old
# Tweets and Threads Posts from downloaded archive files.
# Author: Tinda Zaszcek
# Link: https://github.com/tinnyzaz/PostSearch
# gui.py

import tkinter as tk
import sqlite3

from debug import debug, verbose, error, info
# from database import dbconnect
import config as cfg

# Connect to the SQLite database
conn, db = None, None
tweets = []
# Initialize an index to keep track of the current tweet
index = 0

class GUI:
    def __init__(self, conn, db):
        self.conn = conn
        self.db = db
        self.create_gui()

    def create_gui(self):
        # Create a main window
        self.window = tk.Tk()
        self.window.title("Tweet Viewer")
        self.window.geometry("800x600")
    
        # Configure the row and column weights
        for i in range(6):
            self.window.grid_rowconfigure(i, weight=1)
        for i in range(8):
            self.window.grid_columnconfigure(i, weight=1)

        # Create a Label widget for the search box
        tk.Label(self.window, text="Search:").grid(row=0, column=0, sticky='e', padx=(0, 5), pady=(0, 0))
    
        # Create an Entry widget for the search box
        self.search_entry = tk.Entry(self.window)
        self.search_entry.grid(row=0, column=1, columnspan=5, sticky='ew')
    
        # Create a Search button
        self.search_button = tk.Button(self.window, text="Search", command=self.search_tweets)
        self.search_button.grid(row=0, column=6, sticky='e')
    
        # Create a Clear button
        self.clear_button = tk.Button(self.window, text="Clear", command=self.clear_search)
        self.clear_button.grid(row=0, column=7, sticky='e')
    
        # Create Label widgets with a generic name in the corner cells
        # Label that will display the current tweet / total tweets
        self.index_info = tk.StringVar()
        self.index_info.set("00000/00000")        
        # Create a Label widget with the textvariable option set to the StringVar variable
        tk.Label(self.window, textvariable=self.index_info).grid(row=1, column=0, sticky='s')
        # Label that will display the meta info on this tweet
        self.meta_info = tk.StringVar()
        self.meta_info.set("Meta Info")
        tk.Label(self.window, textvariable=self.meta_info).grid(row=1, column=1, columnspan=6, sticky='sw')
        # Label that will display whether the tweet is archived or not
        tk.Label(self.window, text="Archived?").grid(row=1, column=7, sticky='s')
    
        # Create a Text widget with word wrapping
        self.tweet_text = tk.Text(self.window, wrap=tk.WORD)
        self.tweet_text.grid(row=2, column=0, rowspan=2, columnspan=8)
    
        # Create a Previous button
        self.previous_button = tk.Button(self.window, text="Previous", command=self.previous_tweet)
        self.previous_button.grid(row=4, column=0, sticky='w')
    
        # Create a Copy button
        self.copy_button = tk.Button(self.window, text="Copy", command=self.copy_tweet)
        self.copy_button.grid(row=4, column=1)
    
        # Create an Archive button
        self.archive_button_text = tk.StringVar()
        self.archive_button_text.set("Archive")
        self.archive_button = tk.Button(self.window, text=self.archive_button_text, command=self.archive_tweet)
        self.archive_button.grid(row=4, column=2)
    
        # Create Refresh button
        self.refresh_tweets_button = tk.Button(self.window, text="Refresh", command=self.refresh_tweets)
        self.refresh_tweets_button.grid(row=4, column=3)
    
        # Create a Show Thread button
        self.show_thread_button = tk.Button(self.window, text="Show Thread")
        self.show_thread_button.grid(row=4, column=4)
        self.show_thread_button.config(state=tk.DISABLED)
    
        # Create a Next button
        self.next_button = tk.Button(self.window, text="Next", command=self.next_tweet)
        self.next_button.grid(row=4, column=5, sticky='e')
    
        # Create a Checkbutton widget
        self.show_archived_checkbutton = tk.Checkbutton(self.window, text="Show Archived", variable=cfg.show_archived)
        self.show_archived_checkbutton.grid(row=4, column=6, sticky='e')
    
        # Populate the tweets list
        self.refresh_tweets()
        # Show the first tweet
        self.show_tweet()
    
        # Start the main loop
        self.window.mainloop()

    # Execute a SQL query to get all tweets in order of original date
    def get_tweets(self, query=None):
        base_query = f"SELECT full_text FROM {cfg.table_name}"
        order_by = "ORDER BY created_at"
        search_condition = f"WHERE full_text LIKE '%{query}%'" if query else ""
        archive_condition = "WHERE is_archived = 0" if not cfg.show_archived else ""
    
        if search_condition and archive_condition:
            # Both conditions are present
            conditions = f"{search_condition} AND is_archived = 0"
        elif search_condition or archive_condition:
            # Only one condition is present
            conditions = search_condition or archive_condition
        else:
            # No conditions are present
            conditions = ""
    
        final_query = f"{base_query} {conditions} {order_by}"
    
        try:
            debug("Fetching tweets...")
            self.db.execute(final_query)
            return self.db.fetchall()
        except sqlite3.Error as e:
            error(f"Error executing SQL query: {e}")
            exit(1)

    # Function to copy tweet text to clipboard
    def copy_tweet(self):
        try:
            # Get the current tweet text
            current_tweet = self.tweet_text.get("1.0", tk.END).strip()
            # Copy the tweet text to the clipboard
            self.window.clipboard_clear()
            self.window.clipboard_append(current_tweet)
            info("Copied tweet to clipboard")
        except tk.TclError as e:
            error(f"Error copying tweet to clipboard: {e}")

    # Function to change the text of the Archive button
    def archive_button_check(self, is_archived):
        self.archive_button.config(text="Restore" if is_archived else "Archive")
        if is_archived:
            temp_text = "Restore"
        else:
            temp_text = "Archive"
        self.archive_button_text.set(f"{temp_text}")

    # Call the get_tweets function and store the results in a list
    def refresh_tweets(self):
        global tweets
        tweets = [tweet[0] for tweet in self.get_tweets()]
        debug(f"Fetched {len(tweets)} tweets from database")

    def search_tweets(self):
        query = self.search_entry.get()
        if query:
            debug(f"Searching for tweets with: {query}")
            global tweets
            tweets = [tweet[0] for tweet in self.get_tweets(query)]
            debug(f"Found {len(tweets)} tweets with: {query}")
            # Show the first tweet
            self.show_tweet()
        else:
            info("No search query entered.")
    
    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.refresh_tweets()
        self.show_tweet()

    # Get the is_archive flag of the current tweet
    def is_archived(self):
        try:
            self.db.execute(f"SELECT is_archived FROM {cfg.table_name} WHERE full_text = ?", (tweets[index],))
            return self.db.fetchone()[0]
        except sqlite3.Error as e:
            error(f"Error getting is_archived flag: {e}")
            return False

    # Function to show the current tweet
    def show_tweet(self, index=0):
        # Clear the Text widget
        self.tweet_text.delete('1.0', tk.END)

        # Check if the tweets list is not empty
        if tweets:
            # Insert the current tweet into the Text widget
            self.tweet_text.insert(tk.END, tweets[index])
            debug(f"Showing tweet {index+1}/{len(tweets)}")
            # Update the index info
            self.index_info.set(f"{index+1}/{len(tweets)}")
            # Update the meta info
            self.meta_info.set("Meta Info Placeholder")
            # Update the Archive button text
            self.archive_button_check(self.is_archived())
            debug(f"Updated the labels")
        else:
            debug("No tweets to show.")

    def next_tweet(self):
        global index
        # Increment the index
        index += 1
        # If the index is out of range, set it to the last tweet
        if index >= len(tweets):
            index = len(tweets) - 1
        debug(f"Next tweet: {index+1}/{len(tweets)}")
        # Show the next tweet
        self.show_tweet(index)

    def previous_tweet(self):
        global index
        # Decrement the index
        index -= 1
        # If the index is out of range, set it to the first tweet
        if index < 0:
            index = 0
        debug(f"Previous tweet: {index+1}/{len(tweets)}")
        # Show the previous tweet
        self.show_tweet(index)

    def archive_tweet(self):
        # Get the current tweet
        current_tweet = tweets[index]
        # Toggle the is_archived flag in the database
        try:
            # First, get the current state of is_archived for the tweet
            self.db.execute(f"SELECT is_archived FROM {cfg.table_name} WHERE full_text = ?", (current_tweet,))
            is_archived = self.db.fetchone()[0]
            # Then, toggle the is_archived flag
            is_archived = not bool(is_archived)
            self.db.execute(f"UPDATE {cfg.table_name} SET is_archived = ? WHERE full_text = ?", (is_archived, current_tweet))
            self.conn.commit()
            debug(f"Toggled archive state for tweet: {current_tweet}")
            # Update the text of the Archive button
            self.archive_button_text(is_archived)
        except sqlite3.Error as e:
            error(f"Error toggling archive state for tweet: {e}")

    # # Populate tweet list
    # # refresh_tweets()

    # # Close the connection to the database
    # try:
    #     conn.close()
    #     debug("Database connection closed")
    # except sqlite3.Error as e:
    #     error(f"Error closing database connection: {e}")