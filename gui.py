# self.postsearch - A simple Python application to search through your old
# self.posts and Threads self.posts from downloaded archive files.
# Author: Tinda Zaszcek
# Link: https://github.com/tinnyzaz/PostSearch
# gui.py

import tkinter as tk
import sqlite3

import debug
import config as cfg

from funcs import copy_post, save_user_config, load_user_config
from database import DatabaseConnection

class GUI:
    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.db = db_conn.db
        self.conn = db_conn.conn
        self.posts = []
        self.index = 0
        self.is_archived = False
        self.create_gui()
        # Define your configuration options in a dictionary
        self.userconfig = {
            'using_config': True,
            'show_archived': tk.BooleanVar(value=False),
        }

    def create_gui(self):
        # Create a main window
        self.window = tk.Tk()
        self.window.title("PostSearch")
        self.window.iconbitmap(cfg.ICON_PATH)
        debug.verbose("Creating the main window...")

        # Get the screen width and height
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Define the window size
        window_width = cfg.WINDOW_WIDTH
        window_height = cfg.WINDOW_HEIGHT

        # Calculate the position to center the window
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        debug.verbose("Calculating window position...")

        # Set the window size and position
        self.window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        # Configure the row and column weights
        for i in range(6):
            self.window.grid_rowconfigure(i, weight=1)
        for i in range(8):
                self.window.grid_columnconfigure(i, weight=1)

        debug.verbose("Loading user config options...")
        # Load the user config options
        load_user_config() 
        
        # Create a BooleanVar variable for the Checkbutton widget
        self.check_show_archived = tk.BooleanVar()
        self.check_show_archived.set(cfg.show_archived)

        debug.verbose("Building the primary GUI contents...")
        # Create a Label widget for the search box
        tk.Label(self.window, text="Search:").grid(row=0, column=0, sticky='e', padx=(0, 5), pady=(0, 0))
    
        # Create an Entry widget for the search box
        self.search_entry = tk.Entry(self.window)
        self.search_entry.grid(row=0, column=1, columnspan=5, sticky='ew')
    
        # Create a Search button
        self.search_button = tk.Button(self.window, text="Search", command=self.search_posts)
        self.search_button.grid(row=0, column=6, sticky='e')
    
        # Create a Clear button
        self.clear_button = tk.Button(self.window, text="Clear", command=self.clear_search)
        self.clear_button.grid(row=0, column=7, sticky='e')
    
        # Create Label widgets with a generic name in the corner cells
        # Label that will display the current post / total self.posts
        self.index_info = tk.StringVar()
        self.index_info.set("00000/00000")        
        # Create a Label widget with the textvariable option set to the StringVar variable
        tk.Label(self.window, textvariable=self.index_info).grid(row=1, column=0, sticky='s')
        # Label that will display the meta info on this post
        self.meta_info = tk.StringVar()
        self.meta_info.set("Meta Info")
        tk.Label(self.window, textvariable=self.meta_info).grid(row=1, column=1, columnspan=6, sticky='sw')
        # Label that will display whether the post is archived or not
        tk.Label(self.window, text="Archived?").grid(row=1, column=7, sticky='s')
    
        # Create a Text widget with word wrapping
        self.post_text = tk.Text(self.window, wrap=tk.WORD)
        self.post_text.grid(row=2, column=0, rowspan=2, columnspan=8)
    
        # Create a Previous button
        self.previous_button = tk.Button(self.window, text="Previous", command=self.previous_post)
        self.previous_button.grid(row=4, column=0, sticky='w')
    
        # Create a Copy button
        self.copy_button = tk.Button(self.window, text="Copy", command=lambda: copy_post(self.window, self.post_text.get()))
        self.copy_button.grid(row=4, column=1)
    
        # Create an Archive button
        self.archive_button_text = tk.StringVar()
        self.archive_button_text.set("Archive")
        self.archive_button = tk.Button(self.window, text=self.archive_button_text, command=self.archive_post)
        self.archive_button.grid(row=4, column=2)
    
        # Create Refresh button
        self.refresh_posts_button = tk.Button(self.window, text="Refresh", command=self.refresh_posts)
        self.refresh_posts_button.grid(row=4, column=3)
    
        # Create a Show Thread button
        self.show_thread_button = tk.Button(self.window, text="Show Thread")
        self.show_thread_button.grid(row=4, column=4)
        self.show_thread_button.config(state=tk.DISABLED)
    
        # Create a Next button
        self.next_button = tk.Button(self.window, text="Next", command=self.next_post)
        self.next_button.grid(row=4, column=5, sticky='e')

        # Create a Checkbutton widget
        self.show_archived_checkbutton = tk.Checkbutton(self.window, text="Show Archived", variable=self.show_archived)
        self.show_archived_checkbutton.grid(row=4, column=6, sticky='e')

        debug.verbose("Populating the post list...")
        # Populate the self.posts list
        self.refresh_posts()
        # Show the first post
        self.show_post()
        debug.verbose("Starting the main loop...")
        # Start the main loop
        self.window.mainloop()

    # Function to change the text of the Archive button
    def archive_button_check(self):
        self.archive_button.config(text="Restore" if self.is_archived else "Archive")
        if self.is_archived:
            temp_text = "Restore"
        else:
            temp_text = "Archive"
        self.archive_button_text.set(f"{temp_text}")

    # Call the get_posts function and store the results in a list
    def refresh_posts(self):
        # save the Show Archived setting to user.cfg
        save_user_config(cfg.show_archived.__name__, self.show_archived.get())
        debug.msg("Refreshing posts list...")
        self.posts = [post[0] for post in self.db_conn.get_posts()]
    
    def search_posts(self):
        query = self.search_entry.get()
        if query:
            debug.msg(f"Searching for self.posts with: {query}")
            self.posts = [post[0] for post in self.db_conn.get_posts(query)]
            debug.info(f"Found {len(self.posts)} posts with: {query}")
            # Show the first post
            self.show_post()
        else:
            debug.info("No search query entered.")
    
    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.refresh_posts()
        self.show_post()

    # Get the is_archive flag of the current post
    def post_is_archived(self):
        try:
            self.db.execute(f"SELECT self.is_archived FROM {cfg.table_name} WHERE full_text = ?", (self.posts[index],))
            return self.db.fetchone()[0]
        except sqlite3.Error as e:
            debug.error(f"Error getting self.is_archived flag: {e}")
            return False

    # Function to show the current post
    def show_post(self, index=0):
        # Clear the Text widget
        self.post_text.delete('1.0', tk.END)

        # Check if the self.posts list is not empty
        if self.posts:
            # Insert the current post into the Text widget
            self.post_text.insert(tk.END, self.posts[index])
            debug.msg(f"Showing post {index+1}/{len(self.posts)}")
            # Update the index info
            self.index_info.set(f"{index+1}/{len(self.posts)}")
            # Update the meta info
            self.meta_info.set("Meta Info Placeholder")
            # Update the Archive button text
            self.archive_button_check(self.is_archived())
            debug.msg(f"Updated the labels")
        else:
            debug.msg("No self.posts to show.")

    def next_post(self):
        global index
        # Increment the index
        index += 1
        # If the index is out of range, set it to the last post
        if index >= len(self.posts):
            index = len(self.posts) - 1
        debug.msg(f"Next post: {index+1}/{len(self.posts)}")
        # Show the next post
        self.show_post(index)

    def previous_post(self):
        global index
        # Decrement the index
        index -= 1
        # If the index is out of range, set it to the first post
        if index < 0:
            index = 0
        debug.msg(f"Previous post: {index+1}/{len(self.posts)}")
        # Show the previous post
        self.show_post(index)

    def archive_post(self):
        # Get the current post
        current_post = self.posts[index]
        # Toggle the self.is_archived flag in the database
        try:
            # First, get the current state of self.is_archived for the post
            self.db.execute(f"SELECT self.is_archived FROM {cfg.table_name} WHERE full_text = ?", (current_post,))
            self.is_archived = self.db.fetchone()[0]
            # Then, toggle the self.is_archived flag
            self.is_archived = not bool(self.is_archived)
            self.db.execute(f"UPDATE {cfg.table_name} SET self.is_archived = ? WHERE full_text = ?", (self.is_archived, current_post))
            self.conn.commit()
            debug.msg(f"Toggled archive state for post: {current_post}")
            # Update the text of the Archive button
            self.archive_button_text(self.is_archived)
        except sqlite3.Error as e:
            debug.error(f"Error toggling archive state for post: {e}")
