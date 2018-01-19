from scrapy.spiders import Spider
from scrapy.http import Request

from LianJiaErShouFang.items import LianjiaershoufangItem
import json
from lxml import etree

class ChangShaSpider(Spider):
    name="ChangShaErShouFang"

    download_delay = 0.2

    allowed_domains=[]

    base_url = "https://cs.lianjia.com"

    start_urls=[
        'https://cs.lianjia.com/ershoufang/pg1/'
    ]

    # count = 0

    def parse(self, response):
        """先获得当地所有的地区"""
        sel = etree.HTML(response.text)
        region_list = sel.xpath("//div[@data-role='ershoufang']/div/a/@href")

        for i in range(len(region_list)):
            region = region_list[i]
            print(region)
            url = self.base_url + region + 'pg1/'
            print(url)
            base_url = self.base_url + region
            yield Request(url, meta={'base_url': base_url}, callback=self.parse_region, dont_filter=True)

    def parse_region(self, response):
        """然后根据地区，获取该地区所有的页数"""
        base_url = response.meta['base_url']
        sel = etree.HTML(response.text)
        try:
            # 有的地区可能没有租房信息
            page_info = sel.xpath("//div[@class='page-box house-lst-page-box']/@page-data")[0]
            page_info = json.loads(page_info)
            total_page = page_info.get("totalPage")
        except Exception as e:
            print("Error：", e)
            total_page = 0
        for i in range(int(total_page)):
            url = base_url + 'pg' + str(i+1) + '/'
            print(url)
            yield Request(url, callback=self.parse_ershoufang, dont_filter=True)

    def parse_ershoufang(self, response):
        """获得某一页当中的所有租房信息"""
        # self.count += 1
        # print("正在爬取第%s页" % self.count)
        sel = etree.HTML(response.text)
        ershoufang_list = sel.xpath("//div[@class='info clear']/div[@class='title']/a/@href")
        for ershoufang in ershoufang_list:
            url = ershoufang
            yield Request(url, meta={'url': url}, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        """具体爬取某一个租房信息"""
        url = response.meta['url']
        sel = etree.HTML(response.text)
        item = LianjiaershoufangItem()

        # 房屋名称
        name = sel.xpath("//div[@class='title']/h1[@class='main']/text()")[0]
        item["name"] = name
        # item["name"] = name.split(" ")[0]

        # 房屋总价格
        price = sel.xpath("//div[@class='price ']/span/text()")
        unit = sel.xpath("//div[@class='price ']/span[@class='unit']/span/text()")
        item["price"] = price[0].strip() + unit[0]

        # 房屋单价
        unitPrice = sel.xpath("//div[@class='text']/div[@class='unitPrice']/span[@class='unitPriceValue']/text()")
        unit = sel.xpath("//div[@class='text']/div[@class='unitPrice']/span[@class='unitPriceValue']/i/text()")
        item["unitPrice"] = unitPrice[0] + unit[0]

        # 税费
        # /html/body/div[5]/div[2]/div[2]/div[1]/div[2]/span[1]
        tax = sel.xpath("//div[@class='tax']/span[@class='taxtext']/@title")
        panelTax = sel.xpath("//div[@class='tax']/span[@class='taxtext']/span/span[@id='PanelTax']/text()")
        unit = sel.xpath("//div[@class='tax']/span[@class='taxtext']/span/text()")
        item["tax"] = tax[0] + panelTax[0] + unit[-1].strip().split('(')[0]

        # 房间类型
        room = sel.xpath("//div[@class='houseInfo']/div[@class='room']/div[@class='mainInfo']/text()")
        item["room"] = room[0]

        # 楼层
        floor = sel.xpath("//div[@class='houseInfo']/div[@class='room']/div[@class='subInfo']/text()")
        item["floor"] = floor[0]

        # 方位
        direction = sel.xpath("//div[@class='houseInfo']/div[@class='type']/div[@class='mainInfo']/text()")
        item["direction"] = direction[0]

        # 房屋类型
        type = sel.xpath("//div[@class='houseInfo']/div[@class='type']/div[@class='subInfo']/text()")
        item["type"] = type[0]

        # 面积
        area = sel.xpath("//div[@class='houseInfo']/div[@class='area']/div[@class='mainInfo']/text()")
        item["area"] = area[0]

        # 年份
        year = sel.xpath("//div[@class='houseInfo']/div[@class='area']/div[@class='subInfo']/text()")
        item["year"] = year[0]

        # 小区名称
        communityName = sel.xpath("//div[@class='aroundInfo']/div[@class='communityName']/a[@class='info ']/text()")
        item["communityName"] = communityName[0]

        # 所在区域
        areaName = sel.xpath("//div[@class='aroundInfo']/div[@class='areaName']/span[@class='info']/a/text()")
        item["areaName"] = areaName[0].strip() + areaName[1]

        # 附近地铁
        subway = sel.xpath("//div[@class='aroundInfo']/div[@class='areaName']/a[@class='supplement']/@title")
        item["subway"] = subway[0]

        # 看房时间
        visitTime = sel.xpath("//div[@class='aroundInfo']/div[@class='visitTime']/span[@class='info']/text()")
        item["visitTime"] = visitTime[0]

        # 链家编号
        houseRecord = sel.xpath("//div[@class='aroundInfo']/div[@class='houseRecord']/span[@class='info']/text()")
        item["houseRecord"] = houseRecord[0]

        # 租房链接
        item['url'] = url

        yield item

