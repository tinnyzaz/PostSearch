# PostSearch - A simple Python application to search through your old
# Twitter and Threads posts from downloaded archive files.
# Author: Tinda Zaszcek
# Link: https://github.com/tinnyzaz/PostSearch
# funcs.py

import tkinter as tk

import debug
import config as cfg

from first_run import run_first_time_setup

def check_first_run():
    debug.msg("Checking if this is the first run...")
    try:
        if cfg.FIRST_RUN:
            debug.msg("First run detected.")
            run_first_time_setup()
            return
        debug.msg("Not the first run.")
    except Exception as e:
        debug.error(f"Error checking first run: {e}")
        return

# Function to copy post text to clipboard
def copy_post(window, post_text):
    try:
        # Get the current post text
        current_post = post_text.get("1.0", tk.END).strip()
        # Copy the post text to the clipboard
        window.clipboard_clear()
        window.clipboard_append(current_post)
        debug.info("Copied post to clipboard")
    except tk.TclError as e:
        debug.error(f"Error copying post to clipboard: {e}")

# Function to save user config options
def save_user_config(self):
    # try:
    #     # Open the file in write mode to overwrite existing content
    #     with open(cfg.user_cfg, "w") as file:  
    #         for option_name, option_var in self.userconfig.items():
    #             option_phrase = f"{option_name}={option_var.get()}"
    #             file.write(f"{option_phrase}\n")
    #             debug.info(f"Saved {option_phrase} to {cfg.user_cfg}")
    # except Exception as e:
    #     debug.error(f"Error saving user config: {e}")
    pass

# # Function to load user config options
# def load_user_config(self):
#     # Create a state dictionary to hold the user config options
#     self.state = {}
#     # Open the user config file
#     try:
#         debug.info(f"Loading custom configuration from {cfg.user_cfg}")
#         with open(cfg.user_cfg, "r") as file:
#             # Read the file line by line
#             for line in file:
#                 # Split the line into a key-value pair
#                 key, value = line.strip().split("=")
#                 # Add the key-value pair to the state dictionary
#                 self.state[key] = value
#                 # Overwrite the default value with the user config value
#                 # if the key exists in the user config
#                 cfg.user_config_vars[key] = value
#                 debug.msg(f"Overwrote default value for {key} with {cfg.user_config_vars[key]}")
#     except Exception as e:
#         debug.error(f"Error loading user config: {e}")
#         return

def create_options_checkboxes(window, option_names=None, start_row=5, column_positions=None):
    if option_names is None:
        option_names = cfg.USER_OPTIONS
    if column_positions is None:
        column_positions = [1, 2, 3, 4]
    checkboxes = {}
    for i, name in enumerate(option_names):
        check_var = tk.BooleanVar()
        check_var.set(getattr(cfg, name))
        checkbox = tk.Checkbutton(window, text=name, variable=check_var)
        checkbox.grid(row=start_row, column=column_positions[i], sticky='e')
        checkbox.config(state=tk.DISABLED)
        checkboxes[name] = checkbox
    return checkboxes
