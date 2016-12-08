import json
import os

from common.rating import Rating
from common.redis_client import set_to_redis, get_from_redis
from common.slack_client import post_rating
from playstore.rating_client import load_rating as load_play_rating
from appstore.rating_client import load_rating as load_app_rating


def main():
    package_channels = json.loads(os.environ.get("PACKAGE_CHANNEL"))
    for k, v in package_channels.items():
        print "load rating: {0}, post to #{1}".format(k, v)

        rating = load_play_rating(k)
        try:
            previous_rating = json.loads(
                get_from_redis("{0}_last_rating".format(k)), object_hook=rating_decoder)
        except (TypeError, ValueError):
            previous_rating = Rating()

        for channel in v:
            post_rating(k, channel, rating, previous_rating, "play_store")

        set_to_redis("{0}_last_rating".format(k), json.dumps(rating.__dict__))

    app_id_channels = json.loads(os.environ.get("APP_ID_CHANNEL"))
    for k, v in app_id_channels.items():
        print "load rating: {0}, post to #{1}".format(k, v)

        rating = load_app_rating(k, os.environ.get("APP_FOLLOW_CID"), os.environ.get("APP_FOLLOW_TOKEN"))
        try:
            previous_rating = json.loads(
                get_from_redis("{0}_last_rating".format(k)), object_hook=rating_decoder)
        except (TypeError, ValueError):
            previous_rating = Rating()

        for channel in v:
            post_rating(k, channel, rating, previous_rating, "app_store")

        set_to_redis("{0}_last_rating".format(k), json.dumps(rating.__dict__))


def rating_decoder(obj):
    result = Rating()

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
