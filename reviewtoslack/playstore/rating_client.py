import requests
from lxml import html

from common.rating import Rating

_REQUEST_BASE = "https://play.google.com/store/apps/details?id={0}"


def load_rating(package_name):
    page = requests.get(_REQUEST_BASE.format(package_name))
    tree = html.fromstring(page.content)

    rating = Rating()

    rating.rating_value = float(tree.xpath('//*[@class="score-container"]/*[@itemprop="ratingValue"]/@content')[0])
    rating.rating_count = int(tree.xpath('//*[@class="score-container"]/*[@itemprop="ratingCount"]/@content')[0])

    rating.star_five = int(tree.xpath('//*[@class="rating-bar-container five"]/*[@class="bar-number"]/text()')[0].replace(',', ''))
    rating.star_four = int(tree.xpath('//*[@class="rating-bar-container four"]/*[@class="bar-number"]/text()')[0].replace(',', ''))
    rating.star_three = int(tree.xpath('//*[@class="rating-bar-container three"]/*[@class="bar-number"]/text()')[0].replace(',', ''))
    rating.star_two = int(tree.xpath('//*[@class="rating-bar-container two"]/*[@class="bar-number"]/text()')[0].replace(',', ''))
    rating.star_one = int(tree.xpath('//*[@class="rating-bar-container one"]/*[@class="bar-number"]/text()')[0].replace(',', ''))

    return rating
