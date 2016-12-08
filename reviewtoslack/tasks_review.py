import json
import os

from common.redis_client import set_to_redis, get_from_redis
from common.slack_client import post_review
from playstore.review_client import load_review_list


def main():
    package_channels = json.loads(os.environ.get("PACKAGE_CHANNEL"))
    for k, v in package_channels.items():
        print "load review: {0}, post to #{1}".format(k, v)
        try:
            last_posted_review = int(get_from_redis("{0}_last".format(k)))
        except TypeError:
            last_posted_review = 0

        reviews = load_review_list(k, last_post=last_posted_review)

        for channel in v:
            for review in reviews["list"]:
                if review.lastModified > last_posted_review:
                    post_review(k, channel, review)

        set_to_redis("{0}_last".format(k), reviews["latestModified"])


if __name__ == '__main__':
    main()
