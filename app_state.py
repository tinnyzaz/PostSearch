# PostSearch - A simple Python application to search through your old
# Twitter and Threads posts from downloaded archive files.
# Author: Tinda Zaszcek
# Link: https://github.com/tinnyzaz/PostSearch
# state.py

import configparser
import config as cfg

class AppState:
    def __init__(self):
        # Set state variables for default user preferences
        self.DEBUGGING = cfg.DEBUGGING
        self.VERBOSE = cfg.VERBOSE
        self.FIRST_RUN = cfg.FIRST_RUN
        self.SHOW_ARCHIVED = cfg.SHOW_ARCHIVED

    # Load the user's preferences from the userPrefs.ini file
    def load_user_config(self):
        config = configparser.ConfigParser()
        config.read(cfg.user_cfg)
        for section in config.sections():
            for key, value in config.items(section):
                if hasattr(self, key):
                    # Convert the value to the correct type
                    if value.lower() == 'true':
                        value = True
                    elif value.lower() == 'false':
                        value = False
                    else:
                        try:
                            value = int(value)
                        except ValueError:
                            try:
                                value = float(value)
                            except ValueError:
                                pass  # value is a string, no need to convert
                    setattr(self, key, value)

# Create a global state object that can be imported by other modules
state = AppState()