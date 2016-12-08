import json, urllib2
import hashlib

from common.rating import Rating

_APP_FOLLOW_API = "http://api.appfollow.io/ratings?cid={0}&ext_id={1}&sign={2}"
_SIGN_STRING = "cid={0}ext_id={1}/ratings{2}"


def load_rating(app_id, appfollow_cid, appfollow_token):
    result = urllib2.urlopen(
        _APP_FOLLOW_API.format(appfollow_cid, app_id, sign(app_id, appfollow_cid, appfollow_token)))

    json_result = json.loads(result.read())

    stars1 = int(json_result["ratings"]["list"][0]["stars1"])
    stars2 = int(json_result["ratings"]["list"][0]["stars2"])
    stars3 = int(json_result["ratings"]["list"][0]["stars3"])
    stars4 = int(json_result["ratings"]["list"][0]["stars4"])
    stars5 = int(json_result["ratings"]["list"][0]["stars5"])
    average = (stars1 + stars2 * 2 + stars3 * 3 + stars4 * 4 + stars5 * 5) / float(
        json_result["ratings"]["list"][0]["stars_total"])

    rating = Rating()

    rating.rating_value = average
    rating.rating_count = int(json_result["ratings"]["list"][0]["stars_total"])

    rating.star_five = stars5
    rating.star_four = stars4
    rating.star_three = stars3
    rating.star_two = stars2
    rating.star_one = stars1

    return rating


def sign(app_id, appfollow_cid, appfollow_token):
    return hashlib.md5(_SIGN_STRING.format(appfollow_cid, app_id, appfollow_token)).hexdigest()
