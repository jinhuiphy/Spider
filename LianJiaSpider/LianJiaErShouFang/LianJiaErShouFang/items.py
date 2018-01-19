# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaershoufangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()   # 房屋名称

    price = scrapy.Field()    # 房屋总价
    unitPrice = scrapy.Field()    # 房屋单价
    tax = scrapy.Field()    # 税费

    room = scrapy.Field()    # 房间类型
    floor = scrapy.Field()    # 楼层

    direction = scrapy.Field()    # 方位
    type = scrapy.Field()    # 房屋类型

    area = scrapy.Field()    # 面积
    year = scrapy.Field()    # 年份

    communityName = scrapy.Field()    # 小区名称
    areaName = scrapy.Field()    # 所在区域
    subway = scrapy.Field()    # 附近地铁站

    visitTime = scrapy.Field()    # 看房时间
    houseRecord = scrapy.Field()    # 链家编号

    url = scrapy.Field()    # 租房链接
