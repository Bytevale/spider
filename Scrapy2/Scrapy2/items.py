# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduNewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class DouBan250(scrapy.Item):
    name = scrapy.Field()

class DouBanDesc250(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    short = scrapy.Field()
    people = scrapy.Field()





