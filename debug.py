# PostSearch - A simple Python application to search through your old
# Tweets and Threads Posts from downloaded archive files.
# Author: Tinda Zaszcek
# Link: https://github.com/tinnyzaz/PostSearch
# debug.py

import os, traceback, inspect

import config as cfg
from app_state import state

def msg(*args):
    if cfg.DEBUGGING:
        print(f"{cfg.CYAN}DEBUG:{cfg.RESET}", *args)

def verbose(*args):
    if cfg.VERBOSE:
        print(f"{cfg.LIGHT_GRAY}VERBOSE:{cfg.RESET}", *args)

def warning(*args):
    print(f"{cfg.PINK}WARNING:{cfg.RESET}", *args)

def error(*args):
    try:
        tb = traceback.format_exc()
        print(f"{cfg.ORANGE}ERROR:{cfg.RESET}", *args, "\n", tb)
    except Exception as e:
        print(f"{cfg.ORANGE}ERROR:{cfg.RESET}", *args)
    # try:
    #     # get frame info
    #     frame_info = inspect.stack()[0]
    #     # get line number
    #     lineno = frame_info.lineno
    #     # get function name
    #     script_name = os.path.basename(frame_info.filename)
    #     error_location = f"{cfg.ORANGE}ERROR:{cfg.RESET}", *args, f"at line {lineno} in {script_name}"
    #     error_location = " ".join(error_location)
    #     print(error_location)
    #     print(frame_info)
    # except Exception as e:
    #     print(f"{cfg.ORANGE}ERROR:{cfg.RESET}", *args)

def info(*args):
    print(f"{cfg.NEON_GREEN}INFO:{cfg.RESET}", *args)

def first(*args):
    msg("[FIRST RUN]:", *args)