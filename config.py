# PostSearch - A simple Python application to search through your old
# Tweets and Threads Posts from downloaded archive files.
# Author: Tinda Zaszcek
# Link: https://github.com/tinnyzaz/PostSearch
# config.py

DEBUGGING = True
VERBOSE = True

dbname = "my_tweets.db"
jsonfile = "tweets.json"
table_name = "tweets"
fields = "id_str, created_at, full_text, favorite_count, in_reply_to_status_id_str"

show_archived = False