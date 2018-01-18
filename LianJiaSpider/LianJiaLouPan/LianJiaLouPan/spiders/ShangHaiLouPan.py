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

    download_delay = 0.5

    allowed_domains=[]

    base_url = "http://sh.fang.lianjia.com"

    start_urls=[
        'http://sh.fang.lianjia.com/loupan/pg1'
    ]

    def parse(self, response):
        sel = etree.HTML(response.text)
        # sel = Selector(response)
        total_page = sel.xpath("//div[@class='pagination']/@data-totalpage")[0]
        # page_info = json.loads(page_info)
        # total_page = page_info.get("totalPage")
        print(total_page)
        for i in range(int(total_page)):
            url = self.base_url + '/loupan/pg' + str(i+1)
            print(url)
            yield Request(url, callback=self.parse_loupan)

    def parse_loupan(self, response):
        sel = etree.HTML(response.text)
        loupan_list = sel.xpath("//div[@class='pic-panel']/a/@href")
        for loupan in loupan_list:
            url = self.base_url + loupan
            yield Request(url, callback=lambda response, url=url: self.parse_detail(response, url))

    def parse_detail(self, response, url):
        sel = etree.HTML(response.text)
        item = LianjialoupanItem()

        # 楼盘名称
        name = sel.xpath("//div[@class='title-row']/h1[@class='nameShow']/text()")[0]
        item["name"] = name

        # 楼盘状态
        state = sel.xpath("//div[@class='title-row']/span[@class='status label']/text()")[0]
        item['state'] = state

        # 楼盘网址
        # href = sel.xpath("//div[@class='name-box']/a[@class='clear']/@href")[0]
        # item["url"] = self.base_url + href
        item["url"] = url

        # 楼盘价格
        jiage = sel.xpath("//span[@class='num price']/text()")
        # item["price"] = jiage
        if "已售完" in jiage or "待定" in jiage[0]:
            # junjia = sel.xpath("//span[@class='junjia']/text()")
            # yuan = sel.xpath("span[@class='yuan']/text()")
            item["price"] = jiage[0]
        else:
            unit = sel.xpath("//span[@class='unit price']/text()")
            item["price"] = jiage[0] + unit[0]


        # 物业
        # try:
        #     wuye = sel.xpath("//p[@class='wu-type ']/span/text()")
        #     item['wuye'] = wuye[1]
        # except Exception as e:
        #     wuye = sel.xpath("//p[@class='wu-type manager']/span/text()")
        #     item['wuye'] = wuye[1]
        #     print("Error:", e)
        wuye = sel.xpath("//div[@class='title-row']/span[@class='type label']/text()")[0]
        item["wuye"] = wuye

        # 地址
        # try:
        #     where = sel.xpath("//p[@class='where ']/span/@title")
        #     item["where"] = where[0]
        # except Exception as e:
        #     where = sel.xpath("//p[@class='where manager']/span/@title")
        #     item["where"] = where[0]
        #     print("Error:", e)
        where = sel.xpath("//span[@class='address']/text()")[0]
        item["where"] = where

        yield item
