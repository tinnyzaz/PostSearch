# template_gen.py

from faker import Faker
import json

fake = Faker()

def generate_tweet():
    return {
        "tweet": {
            "edit_info": {
                "initial": {
                    "editTweetIds": [
                        fake.uuid4()
                    ],
                    "editableUntil": fake.date_time_between(start_date='+1y', end_date='+2y').isoformat(),
                    "editsRemaining": str(fake.random_int(min=0, max=5)),
                    "isEditEligible": fake.boolean()
                }
            },
            "retweeted": fake.boolean(),
            "source": "<a href=\"https://mobile.twitter.com\" rel=\"nofollow\">Twitter Web App</a>",
            "entities": {
                "hashtags": [],
                "symbols": [],
                "user_mentions": [
                    {
                        "name": fake.name(),
                        "screen_name": fake.user_name(),
                        "indices": [
                            "0",
                            "13"
                        ],
                        "id_str": fake.uuid4(),
                        "id": fake.uuid4()
                    }
                ],
                "urls": []
            },
            "display_text_range": [
                "0",
                str(fake.random_int(min=0, max=140))
            ],
            "favorite_count": str(fake.random_int(min=0, max=1000)),
            "in_reply_to_status_id_str": fake.uuid4(),
            "id_str": fake.uuid4(),
            "in_reply_to_user_id": fake.uuid4(),
            "truncated": fake.boolean(),
            "retweet_count": str(fake.random_int(min=0, max=1000)),
            "id": fake.uuid4(),
            "in_reply_to_status_id": fake.uuid4(),
            "created_at": fake.date_time_between(start_date='-1y', end_date='now').isoformat(),
            "favorited": fake.boolean(),
            "full_text": fake.sentence(),
            "lang": "en",
            "in_reply_to_screen_name": fake.user_name(),
            "in_reply_to_user_id_str": fake.uuid4()
        }
    }

tweets = [generate_tweet() for _ in range(10)]

with open('tweets.js', 'w') as f:
    f.write('window.YTD.tweets.part0 = ' + json.dumps(tweets, indent=2))