from lxml import html
from rating import Rating
import requests


_REQUEST_BASE = "https://play.google.com/store/apps/details?id={0}"


def load_rating(package_name):
    page = requests.get(_REQUEST_BASE.format(package_name))
    tree = html.fromstring(page.content)

    rating = Rating()

    rating.rating_value = tree.xpath('//*[@class="score-container"]/*[@itemprop="ratingValue"]/@content')[0]
    rating.rating_count = tree.xpath('//*[@class="score-container"]/*[@itemprop="ratingCount"]/@content')[0]

    rating.star_five = tree.xpath('//*[@class="rating-bar-container five"]/*[@class="bar-number"]/text()')[0]
    rating.star_four = tree.xpath('//*[@class="rating-bar-container four"]/*[@class="bar-number"]/text()')[0]
    rating.star_three = tree.xpath('//*[@class="rating-bar-container three"]/*[@class="bar-number"]/text()')[0]
    rating.star_two = tree.xpath('//*[@class="rating-bar-container two"]/*[@class="bar-number"]/text()')[0]
    rating.star_one = tree.xpath('//*[@class="rating-bar-container one"]/*[@class="bar-number"]/text()')[0]

    return rating
