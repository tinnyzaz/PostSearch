# PostSearch - A simple Python application to search through your old
# Tweets and Threads Posts from downloaded archive files.
# Author: Tinda Zaszcek
# Link: https://github.com/tinnyzaz/PostSearch
# config.py

DEBUGGING = True
VERBOSE = True

# ANSI escape codes for colors
CYAN = "\033[96m"
LIGHT_GRAY = "\033[37m"
ORANGE = "\033[33m"
NEON_GREEN = "\033[92m"
PINK = "\033[95m"
RESET = "\033[0m"

dbname = "my_posts.db"
jsonfile_tweets = "tweets.json"
jsonfile_threads = "threads.json"


first_run_check_cfg = 'first_run.cfg'
table_name = "posts"
fields = "id_str, created_at, full_text, favorite_count, in_reply_to_status_id_str"

post_archive_download_path = "/put-archive-zip-here"

archived_tweets_file = "data/tweets.js"     # the location of tweets.js in the archive
# TODO: archived_threads_file = "data/threads.js"   # the location of threads.js in the archive 

show_archived = False