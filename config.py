# PostSearch - A simple Python application to search through your old
# Tweets and Threads Posts from downloaded archive files.
# Author: Tinda Zaszcek
# Link: https://github.com/tinnyzaz/PostSearch
# config.py

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
ICON_PATH = "assets/postsearch.ico"

# ANSI escape codes for colors
CYAN = "\033[96m"
LIGHT_GRAY = "\033[37m"
ORANGE = "\033[33m"
NEON_GREEN = "\033[92m"
PINK = "\033[95m"
RESET = "\033[0m"

dbname = "my_posts.db"
post_archive_download_path = "put-archive-zip-here"
tweet_path = "twitter/data"
threads_path = "instagram/your_instagram_activity/threads"
jsonfile_tweets = "tweets.json"
jsonfile_threads = "threads_and_replies.json" # TODO: Implement this

first_run_check_cfg = 'first_run.cfg'
table_name = "posts"
fields = "id_str, created_at, full_text, favorite_count, in_reply_to_status_id_str"

archived_tweets_file = "data/tweets.js"     # the location of tweets.js in the archive
                                            # that will need to be converted to JSON

show_archived = False

user_cfg = 'user.cfg'

DEBUGGING = True
VERBOSE = False
FIRST_RUN = False

# Define the variables that can be set in the user.cfg file to override
# the defaults
user_config_vars = {
    "show_archived": show_archived,
    "first_run": FIRST_RUN
}
