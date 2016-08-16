import json
import os

from rating_client import load_rating
from reviewtoslack.slack_client import post_rating


def main():
    package_channels = json.loads(os.environ.get("PACKAGE_CHANNEL"))
    for k, v in package_channels.items():
        print "load rating: {0}, post to #{1}".format(k, v)

        rating = load_rating(k)
        post_rating(k, v, rating)


if __name__ == '__main__':
    main()
