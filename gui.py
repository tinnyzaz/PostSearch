# PostSearch - A simple Python application to search through your old
# Twitter and Threads posts from downloaded archive files.
# Author: Tinda Zaszcek
# Link: https://github.com/tinnyzaz/PostSearch
# gui.py

import tkinter as tk
import sqlite3

import debug
import config as cfg

from funcs import ( copy_post, save_user_config, load_user_config, 
                   check_first_run )

class GUI:
    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.posts = []
        self.index = 0
        self.is_archived = False
        self.create_gui()

    def create_gui(self):
        # Create a main window
        self.window = tk.Tk()  # Initialize the root window
        
        # self.SHOW_ARCHIVED = tk.BooleanVar(value=False)
        self.window.title(cfg.WINDOW_TITLE)
        self.window.iconbitmap(cfg.ICON_PATH)

        # Load the user config options
        load_user_config(self) 
    
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
        
        # Check to see if this is the first time the app has run
        check_first_run()
        
        # Create a BooleanVar variable for the DEBUGGING Checkbutton widget
        self.check_DEBUGGING = tk.BooleanVar()
        self.check_DEBUGGING.set(cfg.DEBUGGING)
        # Create a BooleanVar variable for the VERBOSE Checkbutton widget
        self.check_VERBOSE = tk.BooleanVar()
        self.check_VERBOSE.set(cfg.VERBOSE)
        # Create a BooleanVar variable for the FIRST_RUN Checkbutton widget
        self.check_FIRST_RUN = tk.BooleanVar()
        self.check_FIRST_RUN.set(cfg.FIRST_RUN)
        # Create a BooleanVar variable for the SHOW_ARCHIVED Checkbutton widget
        self.check_SHOW_ARCHIVED = tk.BooleanVar()
        self.check_SHOW_ARCHIVED.set(cfg.SHOW_ARCHIVED)

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
        self.is_archived_label = tk.StringVar()
        self.is_archived_label.set("🐵")
        tk.Label(self.window, textvariable=self.is_archived_label, font=("Helvetica", 30)).grid(row=1, column=7, rowspan=2, sticky='n')
    
        # Create a Text widget with word wrapping
        self.post_text = tk.Text(self.window, wrap=tk.WORD)
        self.post_text.grid(row=2, column=0, rowspan=2, columnspan=8)
    
        # Create a Previous button
        self.previous_button = tk.Button(self.window, text="Previous", command=self.previous_post)
        self.previous_button.grid(row=4, column=1, sticky='w')
    
        # Create a Copy button
        self.copy_button = tk.Button(self.window, text="Copy", command=lambda: copy_post(self.window, self.post_text.get()))
        self.copy_button.grid(row=4, column=2)
    
        # Create an Archive button
        self.archive_button_text = tk.StringVar()
        self.archive_button_text.set("Hide Post")
        self.archive_button = tk.Button(self.window, text=self.archive_button_text, command=self.archive_post)
        self.archive_button.grid(row=4, column=3)
    
        # Create Refresh button
        self.populate_posts_button = tk.Button(self.window, text="Refresh", command=self.populate_posts)
        self.populate_posts_button.grid(row=4, column=4)
    
        # Create a Show Thread button
        self.show_thread_button = tk.Button(self.window, text="Show Thread")
        self.show_thread_button.grid(row=4, column=5)
        self.show_thread_button.config(state=tk.DISABLED)
    
        # Create a Next button
        self.next_button = tk.Button(self.window, text="Next", command=self.next_post)
        self.next_button.grid(row=4, column=6, sticky='e')

        # These checkbuttons are disabled for now, but will toggle user config options
        # Create a DEBUGGING Checkbutton widget
        self.DEBUGGING_checkbutton = tk.Checkbutton(self.window, text="DEBUGGING", variable=self.check_DEBUGGING)
        self.DEBUGGING_checkbutton.grid(row=5, column=1, sticky='e')
        self.DEBUGGING_checkbutton.config(state=tk.DISABLED)
        # Create a VERBOSE Checkbutton widget
        self.VERBOSE_checkbutton = tk.Checkbutton(self.window, text="VERBOSE", variable=self.check_VERBOSE)
        self.VERBOSE_checkbutton.grid(row=5, column=2, sticky='e')
        self.VERBOSE_checkbutton.config(state=tk.DISABLED)
        # Create a SHOW_ARCHIVED Checkbutton widget
        self.SHOW_ARCHIVED_checkbutton = tk.Checkbutton(self.window, text="Show Hidden Posts", variable=self.check_SHOW_ARCHIVED)
        self.SHOW_ARCHIVED_checkbutton.grid(row=5, column=3, sticky='e')
        self.SHOW_ARCHIVED_checkbutton.config(state=tk.DISABLED)
        # Create a FIRST_RUN Checkbutton widget
        self.FIRST_RUN_checkbutton = tk.Checkbutton(self.window, text="First Run", variable=self.check_FIRST_RUN)
        self.FIRST_RUN_checkbutton.grid(row=5, column=4, sticky='e')
        self.FIRST_RUN_checkbutton.config(state=tk.DISABLED)

        self.populate_posts()
        # Show the first post
        self.show_post()
        debug.verbose("Starting the main loop...")
        # Start the main loop
        self.window.mainloop()

    # Call the get_posts function and store the results in a list
    def populate_posts(self):
        # save the Show Archived setting to user.cfg
        save_user_config(self)  # this doesn't do anything yet
        debug.msg("Populating posts list...")
        # self.posts = [post[0] for post in self.db_conn.get_posts()]
        self.posts = self.db_conn.get_posts()
    
    def search_posts(self):
        query = self.search_entry.get()
        if query:
            debug.msg(f"Searching for self.posts with: {query}")
            # self.posts = [post[2] for post in self.db_conn.get_posts(query)]
            self.posts = self.db_conn.get_posts(query)
            debug.msg(self.posts)
            debug.info(f"Found {len(self.posts)} posts with: {query}")
            # Show the first post
            self.show_post()
        else:
            debug.info("No search query entered.")
    
    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.populate_posts()
        self.show_post()

    # Get the is_archive flag of the current post
    def post_is_archived(self):
        try:
            self.db_conn.db.execute(f"SELECT self.is_archived FROM {cfg.table_name} WHERE full_text = ?", (self.posts[self.index],))
            return self.db_conn.db.fetchone()[0]
        except sqlite3.Error as e:
            debug.error(f"Error getting self.is_archived flag: {e}")
            return False

    # Function to change the text of the Archive button
    def archive_button_check(self, postarchived=False):
        # TODO: this function is not working
        self.archive_button.config(text="Unhide Post" if self.is_archived else "Hide Post")
        if postarchived:
            temp_text = "Show Post"
        else:
            temp_text = "Hide Post"
        self.archive_button_text.set(f"{temp_text}")

    # Function to show the current post
    def show_post(self, which=0):
        # Clear the Text widget
        self.post_text.delete('1.0', tk.END)
        self.index = which
        # Check if the self.posts list is not empty
        if self.posts:
            # Insert the current post into the Text widget
            self.post_text.insert(tk.END, self.posts[self.index][2])
            debug.msg(f"Showing post {self.index+1}/{len(self.posts)}")
            # Update the self.index info
            self.index_info.set(f"{self.index+1:05}/{len(self.posts):05}")
            # Update the meta info
            postid = self.posts[self.index][0]
            postdate = self.posts[self.index][1]
            postfavs = self.posts[self.index][3]
            postreply = self.posts[self.index][4]
            postarchived = self.posts[self.index][5]

            if postreply:
                postreplyto = f"| Reply to {postreply}"
            else:
                postreplyto = ""
            self.meta_info.set(f"ID: {postid} | {postdate} | 💜{postfavs} {postreplyto}")
            # Update the Archive button text using 🙈 and 🐵
            self.archive_button_check(postarchived)
            debug.msg(f"Updated the labels")
        else:
            debug.msg("No posts to show.")

    def next_post(self):
        # Increment the self.index
        self.index += 1
        # If the self.index is out of range, set it to the last post
        if self.index >= len(self.posts):
            self.index = len(self.posts) - 1
        debug.msg(f"Next post: {self.index+1}/{len(self.posts)}")
        # Show the next post
        self.show_post(self.index)

    def previous_post(self):
        # Decrement the self.index
        self.index -= 1
        # If the self.index is out of range, set it to the first post
        if self.index < 0:
            self.index = 0
        debug.msg(f"Previous post: {self.index+1}/{len(self.posts)}")
        # Show the previous post
        self.show_post(self.index)

    def archive_post(self):
        # Get the current post
        current_post = self.posts[self.index]
        # Toggle the self.is_archived flag in the database
        try:
            # First, get the current state of self.is_archived for the post
            self.db_conn.db.execute(f"SELECT self.is_archived FROM {cfg.table_name} WHERE full_text = ?", (current_post,))
            self.is_archived = self.db_conn.db.fetchone()[0]
            # Then, toggle the self.is_archived flag
            self.is_archived = not bool(self.is_archived)
            self.db_conn.db.execute(f"UPDATE {cfg.table_name} SET self.is_archived = ? WHERE full_text = ?", (self.is_archived, current_post))
            self.db_conn.conn.commit()
            debug.msg(f"Toggled archive state for post: {current_post}")
            # Update the text of the Archive button
            self.archive_button_text(self.is_archived)
        except sqlite3.Error as e:
            debug.error(f"Error toggling archive state for post: {e}")
