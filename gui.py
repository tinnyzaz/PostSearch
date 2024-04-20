# PostSearch - A simple Python application to search through your old
# Twitter and Threads posts from downloaded archive files.
# Author: Tinda Zaszcek
# Link: https://github.com/tinnyzaz/PostSearch
# gui.py

import tkinter as tk
import sqlite3

import debug
import funcs
import config as cfg

from app_state import state
from version import version

class GUI:
    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.posts = []
        self.index = 0
        self.is_archived = False
        self.create_gui()

    def create_gui(self):
        # Initialize the root window
        self.window = self.create_window()    
        debug.verbose("Creating the main window...")
        self.populate_the_gui()
    
    def create_window(self):
        window = tk.Tk()
        window.withdraw()  # Hide the window

        window.title(cfg.WINDOW_TITLE + f" v{version}")
        window.iconbitmap(cfg.ICON_PATH)

        # Get the screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Define the window size
        window_width = cfg.WINDOW_WIDTH
        window_height = cfg.WINDOW_HEIGHT

        # Calculate the position to center the window
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Set the window size and position
        window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        window.deiconify()  # Show the window

        return window

    def populate_the_gui(self):
        # Configure the row and column weights
        for i in range(6):
            self.window.grid_rowconfigure(i, weight=1)
        for i in range(8):
            self.window.grid_columnconfigure(i, weight=1)
        
        # Check to see if this is the first time the app has run
        funcs.check_first_run()
        # TODO: is the the best place to do this?

        debug.verbose("Building the primary GUI contents...")
        # Create a Label widget for the search box
        tk.Label(self.window, text="Search:").grid(row=0, column=0, sticky='e', padx=(0, 5), pady=(0, 0))
    
        # Create an Entry widget for the search box
        self.search_entry = tk.Entry(self.window)
        self.search_entry.grid(row=0, column=1, columnspan=5, sticky='ew')
        
        # Bind the Enter key to the search_posts method
        self.search_entry.bind('<Return>', lambda event: self.search_posts())
        
        # Create a Search button
        self.search_button = tk.Button(self.window, text="Search", width=cfg.TOP_BUTTON_WIDTH, command=self.search_posts)
        self.search_button.grid(row=0, column=6, padx=6)
        
        # Create a Clear button
        self.clear_button = tk.Button(self.window, text="Reset", width=cfg.TOP_BUTTON_WIDTH, command=self.clear_search)
        self.clear_button.grid(row=0, column=7, sticky='w')
    
        # Label that will display the current post / total self.posts
        self.index_info = tk.StringVar()
        self.index_info.set("00000/00000")        
        
        # Create a Label widget with the textvariable option set to the StringVar variable
        tk.Label(self.window, textvariable=self.index_info).grid(row=1, column=0, sticky='s')
        
        # Label that will display the meta info on this post
        self.meta_info = tk.StringVar()
        self.meta_info.set("Meta Info")
        tk.Label(self.window, textvariable=self.meta_info).grid(row=1, column=1, columnspan=6, sticky='sw')

        # SIDE BAR (LEFT) ============================================================
        # Create the Side Bar Frame
        self.side_bar_frame = tk.Frame(self.window)
        self.side_bar_frame.grid(row=2, column=0, rowspan=1)

        # Create a small text input for the user to enter a post ID
        self.post_id_entry = tk.Entry(self.side_bar_frame, width=6)
        self.post_id_entry.grid(row=0, column=0, sticky='s')
        
        # Bind the Enter key to the GO box
        self.post_id_entry.bind('<Return>', lambda event: self.go_action())

        # Create a Go button
        self.go_button = tk.Button(self.side_bar_frame, text="Go", width=cfg.SIDE_BUTTON_WIDTH, command=self.go_action)
        self.go_button.grid(row=1, column=0, sticky='s')

        # Create a First Button
        self.first_button = tk.Button(self.side_bar_frame, text="First", width=cfg.SIDE_BUTTON_WIDTH, command=lambda: self.show_post(0))
        self.first_button.grid(row=2, column=0, sticky='s')

        # Create a Last Button
        self.last_button = tk.Button(self.side_bar_frame, text="Last", width=cfg.SIDE_BUTTON_WIDTH, command=lambda: self.show_post(len(self.posts)-1))
        self.last_button.grid(row=3, column=0, sticky='s')
        
        # Create a Copy button
        self.copy_button = tk.Button(self.side_bar_frame, text="Copy", width=cfg.SIDE_BUTTON_WIDTH, command=lambda: funcs.copy_post(self.window, self.post_text))
        self.copy_button.grid(row=4, column=0, sticky='s')

        # SIDE BAR (RIGHT) ===========================================================
        # Label that will display whether the post is archived or not
        self.is_archived_label = tk.StringVar()
        self.is_archived_label.set("🐵")
        tk.Label(self.window, textvariable=self.is_archived_label, font=("Helvetica", 30)).grid(row=1, column=7, rowspan=2, sticky='n')
    
        # MAIN CONTENT ==============================================================
        # Create a Text widget with word wrapping
        self.post_text = tk.Text(self.window, wrap=tk.WORD)
        self.post_text.grid(row=2, column=0, rowspan=2, columnspan=8)
    
        # BOTTOM BAR ================================================================
        # Create a Previous button
        self.previous_button = tk.Button(self.window, text="Previous", command=self.previous_post, width=cfg.BOTTOM_BUTTON_WIDTH)
        self.previous_button.grid(row=4, column=1, sticky='sw')

        # Create an Archive button
        self.archive_button_text = tk.StringVar()
        self.archive_button_text.set("Hide Post")
        self.archive_button = tk.Button(self.window, textvariable=self.archive_button_text, command=self.archive_post, width=cfg.BOTTOM_BUTTON_WIDTH)
        self.archive_button.grid(row=4, column=3, sticky='s')

        # Create Refresh button
        self.populate_posts_button = tk.Button(self.window, text="Refresh", command=self.populate_posts, width=cfg.BOTTOM_BUTTON_WIDTH)
        self.populate_posts_button.grid(row=4, column=4, sticky='s')
    
        # Create a Show Thread button
        self.show_thread_button = tk.Button(self.window, text="Show Thread", width=cfg.BOTTOM_BUTTON_WIDTH)
        self.show_thread_button.grid(row=4, column=5, sticky='s')
        self.show_thread_button.config(state=tk.DISABLED)
    
        # Create a Next button
        self.next_button = tk.Button(self.window, text="Next", command=self.next_post, width=cfg.BOTTOM_BUTTON_WIDTH)
        self.next_button.grid(row=4, column=6, sticky='se')

        self.checkboxes = funcs.create_options_checkboxes(self.window)

        self.populate_posts()
        # Show the first post
        self.show_post()
        debug.verbose("Starting the main loop...")
        # Start the main loop
        self.window.mainloop()

    def go_action(self):
        post_id = int(self.post_id_entry.get()) - 1
        self.show_post(post_id)
        self.post_id_entry.delete(0, 'end')

    # Call the get_posts function and store the results in a list
    def populate_posts(self):
        # save the Show Archived setting to user.cfg
        funcs.save_user_config(self)  # this doesn't do anything yet
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
            self.postid = self.posts[self.index][0]
            postdate = self.posts[self.index][1]
            postfavs = self.posts[self.index][3]
            postreply = self.posts[self.index][4]
            postarchived = self.posts[self.index][5]
            
            # Make sure our instance variable is updated
            self.is_archived = postarchived if postarchived is not None else False

            # If this post is in reply to another, show that post's ID
            if postreply:
                postreplyto = f"| Reply to {postreply}"
                # And we will want to figure out if this post is part of a thread.
            else:
                postreplyto = ""
            self.meta_info.set(f"ID: {self.postid} | {postdate} | 💜{postfavs} {postreplyto}")
            
            self.archive_button_text_toggle()
            
            # Update the Archived label using 🙈 and 🐵
            # self.is_archived_label.set(f"{self.archived_icon_toggle(postarchived)}")
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
        # Toggle the self.is_archived flag in the database
        try:
            # First, get the current state of self.is_archived for the post
            self.db_conn.db.execute(f"SELECT is_archived FROM {cfg.table_name} WHERE id_str = ?", (self.postid,))
            self.is_archived = self.db_conn.db.fetchone()[0]
            # Then, toggle the self.is_archived flag
            self.is_archived = not bool(self.is_archived)
            # Finally, update the database with the new self.is_archived flag
            self.db_conn.db.execute(f"UPDATE {cfg.table_name} SET is_archived = ? WHERE id_str = ?", (self.is_archived, self.postid))
            self.db_conn.conn.commit()
            debug.msg(f"Toggled archive state to {self.is_archived} for post: {self.postid}")
            # Update the text of the Archive button
            self.archive_button_text_toggle()
        except sqlite3.Error as e:
            debug.error(f"Error toggling archive state for post: {e}")

    # Function to change the text of the Archive button
    def archive_button_text_toggle(self):
        button_text = "Unhide Post" if self.is_archived else "Hide Post"
        self.archive_button_text.set(button_text)
        archive_icon = "🙈" if self.is_archived else "🐵"
        self.is_archived_label.set(f"{archive_icon}")

    # def archived_icon_toggle():
    #     debug.msg("This post is archived." if self.is_archived else "This post is not archived.")
    #     return "🙈" if self.is_archived else "🐵"

if __name__ == "__main__":
    debug.warning("This script is not meant to be run directly.")
    exit(1)