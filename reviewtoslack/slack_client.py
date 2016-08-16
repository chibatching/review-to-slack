import os
from slacker import Slacker

_SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
_ACCOUNT_ID = os.environ.get("PLAY_ACCOUNT_ID")
_REVIEW_DETAIL_URL = "https://play.google.com/apps/publish/?dev_acc={0}#ReviewDetailsPlace:p={1}&reviewid={2}"
_RATING_DETAIL_URL = "https://play.google.com/apps/publish/?dev_acc={0}#RatingsPlace:p={1}"
_COLOR = ["#d36259", "#ef7e14", "#ffc105", "#bfd047", "#0e9d58"]


def post_review(package, channel, review):
    star = ""
    for i in range(0, review.starRating):
        star += ":star:"

    attachment = [
        {
            "pretext": star,
            "author_name": review.userName,
            "title": review.title if review.title is not None else "No title",
            "title_link": _REVIEW_DETAIL_URL.format(_ACCOUNT_ID, package, review.reviewId),
            "text": review.text,
            "mrkdwn_in": ["text"],
            "color": _COLOR[review.starRating - 1],
            "fields": [
                {
                    "title": "App version",
                    "value": "{0} ({1})".format(review.appVersionName, review.appVersionCode),
                    "short": True
                },
                {
                    "title": "Device",
                    "value": review.device,
                    "short": True
                },
                {
                    "title": "Android version",
                    "value": review.androidOsVersion,
                    "short": True
                }
            ]
        }
    ]

    slacker = Slacker(_SLACK_TOKEN)
    slacker.chat.post_message(channel, "", as_user=True, attachments=attachment)


def post_rating(package, channel, rating):
    text = """Rating count = {0}
:star::star::star::star::star:  {1}
:star::star::star::star:  {2}
:star::star::star:  {3}
:star::star:  {4}
:star:  {5}
""".format(rating.rating_count, rating.star_five, rating.star_four, rating.star_three, rating.star_two, rating.star_one)

    attachment = [
        {
            "title": "Rating average = {0}".format(rating.rating_value),
            "title_link": _RATING_DETAIL_URL.format(_ACCOUNT_ID, package),
            "text": text,
            "color": "#0e9d58"
        }
    ]

    slacker = Slacker(_SLACK_TOKEN)
    slacker.chat.post_message(channel, "", as_user=True, attachments=attachment)
