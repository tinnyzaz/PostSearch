# PostSearch - A simple Python application to search through your old
# Twitter and Threads posts from downloaded archive files.
# Author: Tinda Zaszcek
# Link: https://github.com/tinnyzaz/PostSearch
# utils/shortcuts.py
import debug
import config as cfg


# a shortcut function for simple try/except blocks
def try_this(func, *args, **kwargs):
    try:
        debug.msg(f"{cfg.PURPLE}[TRY_THIS] Running {func}{cfg.RESET}")
        func(*args, **kwargs)
        return True
    except Exception as e:
        debug.error(f"{cfg.PURPLE}[TRY_THIS] Error in {func}: {e}{cfg.RESET}")
        return False