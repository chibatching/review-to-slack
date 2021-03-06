import os

from slacker import Slacker

_SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
_ACCOUNT_ID = os.environ.get("PLAY_ACCOUNT_ID")
_REVIEW_DETAIL_URL = "https://play.google.com/apps/publish/?dev_acc={0}#ReviewDetailsPlace:p={1}&reviewid={2}"
_RATING_DETAIL_URL = "https://play.google.com/apps/publish/?dev_acc={0}#RatingsPlace:p={1}"
_COLOR = ["#d36259", "#ef7e14", "#ffc105", "#bfd047", "#0e9d58"]

_PLAY_STORE_ICON_URL = "https://raw.githubusercontent.com/chibatching/review-to-slack/master/images/play-store-icon.png"
_APP_STORE_ICON_URL = "https://raw.githubusercontent.com/chibatching/review-to-slack/master/images/app-store-icon.png"


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


def post_rating(package, channel, rating, previous_rating, store):
    attachment_text = """:star::star::star::star::star:  {0} ({5:+})
:star::star::star::star:  {1} ({6:+})
:star::star::star:  {2} ({7:+})
:star::star:  {3} ({8:+})
:star:  {4} ({9:+})""".format(rating.star_five, rating.star_four, rating.star_three, rating.star_two, rating.star_one,
                              rating.star_five - previous_rating.star_five,
                              rating.star_four - previous_rating.star_four,
                              rating.star_three - previous_rating.star_three,
                              rating.star_two - previous_rating.star_two,
                              rating.star_one - previous_rating.star_one)

    text = """Rating average = {0} ({1:+})
Rating count = {2} ({3:+})""".format(round(rating.rating_value, 4),
                                     round(rating.rating_value - previous_rating.rating_value, 4),
                                     rating.rating_count, rating.rating_count - previous_rating.rating_count)

    attachment = [
        {
            "text": attachment_text,
            "color": "#0e9d58",
        }
    ]

    icon = _PLAY_STORE_ICON_URL if (store == "play_store") else _APP_STORE_ICON_URL if (store == "app_store") else None
    user_name = "Play Store Rating" if (store == "play_store")\
        else "App Store Rating" if (store == "app_store") else None

    slacker = Slacker(_SLACK_TOKEN)
    slacker.chat.post_message(channel, text, attachments=attachment, username=user_name, icon_url=icon)
