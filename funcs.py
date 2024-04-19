# funcs.py
import os
import tkinter as tk

import debug
import config as cfg

from first_run import run_first_time_setup

def check_first_run():
    debug.msg("Checking if this is the first run...")
    try:
        # Check if the first run check file exists
        if os.path.exists(cfg.first_run_check_cfg):
            debug.msg(f"First run check file found: {cfg.first_run_check_cfg}")
            # Check the contents of the first run check file
            with open(cfg.first_run_check_cfg, "r") as file:
                verify_first_run = file.read().strip()
                if verify_first_run == "False":
                    # We're looking for the string "False" to verify the first run check file
                    debug.msg("First run check file found and verified.")
                    return False
        # If the file does not exist or does not contain "False", run the first run setup
        debug.msg(f"First run check file not found or not verified: {cfg.first_run_check_cfg}")
        run_first_time_setup()
        return
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