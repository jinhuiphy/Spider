# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjialoupanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    state = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    wuye = scrapy.Field()
    where = scrapy.Field()


