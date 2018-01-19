# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiazufangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    price = scrapy.Field()
    name = scrapy.Field()
    area = scrapy.Field()
    type = scrapy.Field()
    floor = scrapy.Field()
    direction = scrapy.Field()
    subway = scrapy.Field()
    community = scrapy.Field()
    location = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()

