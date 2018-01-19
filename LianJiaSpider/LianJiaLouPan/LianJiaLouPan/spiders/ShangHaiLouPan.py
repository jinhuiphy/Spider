from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import Rule,CrawlSpider
from scrapy.linkextractors import LinkExtractor

from LianJiaLouPan.items import LianjialoupanItem
import json
from lxml import etree

class ChangShaSpider(Spider):
    name="ShangHaiLouPan"

    download_delay = 0.3

    allowed_domains=[]

    base_url = "http://sh.fang.lianjia.com"

    start_urls=[
        'http://sh.fang.lianjia.com/loupan/pg1/'
    ]

    def parse(self, response):
        """获取总页数对应的url"""

        sel = etree.HTML(response.text)
        total_page = sel.xpath("//div[@class='pagination']/@data-totalpage")[0]
        print(total_page)
        for i in range(int(total_page)):
            url = self.base_url + '/loupan/pg' + str(i+1) + '/'
            print(url)
            yield Request(url, callback=self.parse_loupan, dont_filter=True)

    def parse_loupan(self, response):
        """获取每一页相应楼盘对应的url"""

        sel = etree.HTML(response.text)
        loupan_list = sel.xpath("//div[@class='pic-panel']/a/@href")
        for loupan in loupan_list:
            url = self.base_url + loupan
            yield Request(url, meta={'url': url}, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        """具体处理获取某一个楼盘的信息"""

        url = response.meta['url']
        sel = etree.HTML(response.text)
        item = LianjialoupanItem()

        # 楼盘名称
        name = sel.xpath("//div[@class='title-row']/h1[@class='nameShow']/text()")[0]
        item["name"] = name

        # 楼盘状态
        state = sel.xpath("//div[@class='title-row']/span[@class='status label']/text()")[0]
        item['state'] = state

        # 楼盘网址
        item["url"] = url

        # 楼盘价格
        jiage = sel.xpath("//span[@class='num price']/text()")
        if "已售完" in jiage or "待定" in jiage[0]:
            item["price"] = jiage[0]
        else:
            unit = sel.xpath("//span[@class='unit price']/text()")
            item["price"] = jiage[0] + unit[0]

        # 物业
        wuye = sel.xpath("//div[@class='title-row']/span[@class='type label']/text()")[0]
        item["wuye"] = wuye

        # 地址
        where = sel.xpath("//span[@class='address']/text()")[0]
        item["where"] = where

        yield item
