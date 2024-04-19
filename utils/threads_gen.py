import json
from faker import Faker
import random

fake = Faker()

def generate_post():
    return {
        "media": [
            {
                "uri": fake.file_path(extension="jpg") if random.choice([True, False]) else "",
                "creation_timestamp": fake.unix_time(),
                "media_metadata": {
                    "photo_metadata": {
                        "exif_data": [
                            {
                                "device_id": "android-" + fake.md5(),
                                "source_type": str(random.randint(1, 5))
                            }
                        ]
                    } if random.choice([True, False]) else {},
                    "camera_metadata": {
                        "has_camera_metadata": fake.boolean()
                    }
                },
                "title": fake.sentence(),
                "cross_post_source": {
                    "source_app": "FB"
                }
            }
        ]
    }

def generate_data():
    return {
        "text_post_app_text_posts": [generate_post() for _ in range(10)]
    }

data = generate_data()

with open('threads_and_replies.json', 'w') as f:
    json.dump(data, f, indent=2)