# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PYGWItem(scrapy.Item):
    name = scrapy.Field()
    job = scrapy.Field()
    gwzz = scrapy.Field()
