import json
import os

from rating_client import load_rating
from rating import Rating
from reviewtoslack.slack_client import post_rating
import redis_client


def main():
    package_channels = json.loads(os.environ.get("PACKAGE_CHANNEL"))
    for k, v in package_channels.items():
        print "load rating: {0}, post to #{1}".format(k, v)

        rating = load_rating(k)
        try:
            previous_rating = json.loads(
                redis_client.get_from_redis("{0}_last_rating".format(k)), object_hook=rating_decoder)
        except (TypeError, ValueError):
            previous_rating = Rating()

        print previous_rating

        for channel in v:
            post_rating(k, channel, rating, previous_rating)

        redis_client.set_to_redis("{0}_last_rating".format(k), json.dumps(rating.__dict__))


def rating_decoder(obj):
    result = Rating()

    if obj is not None:
        result.rating_value = obj['rating_value']
        result.rating_count = obj['rating_count']
        result.star_five = obj['star_five']
        result.star_four = obj['star_four']
        result.star_three = obj['star_three']
        result.star_two = obj['star_two']
        result.star_one = obj['star_one']

    return result


if __name__ == '__main__':
    main()
