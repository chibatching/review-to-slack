import json
import os

import redis_client
from review_client import load_review_list
from reviewtoslack.slack_client import post_review


def main():
    package_channels = json.loads(os.environ.get("PACKAGE_CHANNEL"))
    for k, v in package_channels.items():
        print "load review: {0}, post to #{1}".format(k, v)
        try:
            last_posted_review = int(redis_client.get_from_redis("{0}_last".format(k)))
        except TypeError:
            last_posted_review = 0

        reviews = load_review_list(k, last_post=last_posted_review)

        for review in reviews["list"]:
            if review.lastModified > last_posted_review:
                post_review(k, v, review)

        redis_client.set_to_redis("{0}_last".format(k), reviews["latestModified"])


if __name__ == '__main__':
    main()
