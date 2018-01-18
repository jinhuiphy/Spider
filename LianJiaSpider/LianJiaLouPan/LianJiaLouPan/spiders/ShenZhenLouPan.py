from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import Rule,CrawlSpider
from scrapy.linkextractors import LinkExtractor

from LianJiaLouPan.items import LianjialoupanItem
import json
from lxml import etree

class ShenZhenSpider(Spider):
    # 切记去修改数据库的名字
    name="ShenZhenLouPan"

    download_delay = 0.6

    allowed_domains=[]

    base_url = "https://sz.fang.lianjia.com"

    start_urls=[
        'https://sz.fang.lianjia.com/loupan/pg1'
    ]

    def parse(self, response):
        sel = etree.HTML(response.text)
        # sel = Selector(response)
        page_info = sel.xpath("//div[@class='page-box house-lst-page-box']/@page-data")[0]
        page_info = json.loads(page_info)
        total_page = page_info.get("totalPage")
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
            yield Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        sel = etree.HTML(response.text)
        item = LianjialoupanItem()

        # 楼盘名称
        name = sel.xpath("//div[@class='name-box']/a[@class='clear']/@title")[0]
        item["name"] = name

        # 楼盘状态
        state = sel.xpath("//div[@class='name-box']/div[@class='state-div']/span[@class='state']/text()")[0]
        item['state'] = state

        # 楼盘网址
        href = sel.xpath("//div[@class='name-box']/a[@class='clear']/@href")[0]
        item["url"] = self.base_url + href

        # 楼盘价格
        jiage = sel.xpath("//div[@class='box-left-top']/p[@class='jiage']/span/text()")
        # item["price"] = jiage
        if "均价" in jiage:
            # junjia = sel.xpath("//span[@class='junjia']/text()")
            # yuan = sel.xpath("span[@class='yuan']/text()")
            item["price"] = jiage[1] + jiage[2]
        else:
            item["price"] = jiage[0]

        # 物业
        try:
            wuye = sel.xpath("//p[@class='wu-type ']/span/text()")
            item['wuye'] = wuye[1]
        except Exception as e:
            wuye = sel.xpath("//p[@class='wu-type manager']/span/text()")
            item['wuye'] = wuye[1]
            print("Error:", e)

        # 地址
        try:
            where = sel.xpath("//p[@class='where ']/span/@title")
            item["where"] = where[0]
        except Exception as e:
            where = sel.xpath("//p[@class='where manager']/span/@title")
            item["where"] = where[0]
            print("Error:", e)

        yield item
