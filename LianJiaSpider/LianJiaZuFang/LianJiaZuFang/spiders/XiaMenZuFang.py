from scrapy.spiders import Spider
from scrapy.http import Request

from LianJiaZuFang.items import LianjiazufangItem
import json
from lxml import etree

class ChangShaSpider(Spider):
    name="XiaMenZuFang"

    download_delay = 0.2

    allowed_domains=[]

    base_url = "https://xm.lianjia.com"

    start_urls=[
        'https://xm.lianjia.com/zufang/pg1/'
    ]

    count = 0

    def parse(self, response):
        """先获得当地所有的地区"""
        sel = etree.HTML(response.text)
        region_list = sel.xpath("//dd[@data-index='0']/div[@class='option-list']/a/@href")
        for i in range(1, len(region_list)):
            region = region_list[i]
            print(region)
            url = self.base_url + region + 'pg1/'
            print(url)
            base_url = self.base_url + region
            yield Request(url, meta={'base_url':base_url}, callback=self.parse_region, dont_filter=True)

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
            yield Request(url, callback=self.parse_zufang, dont_filter=True)

    def parse_zufang(self, response):
        """获得某一页当中的所有租房信息"""
        self.count += 1
        print("正在爬取第%s页" % self.count)
        sel = etree.HTML(response.text)
        zufang_list = sel.xpath("//div[@class='pic-panel']/a/@href")
        for zufang in zufang_list:
            url = zufang
            yield Request(url, meta={'url': url}, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        """具体爬取某一个租房信息"""
        url = response.meta['url']
        sel = etree.HTML(response.text)
        item = LianjiazufangItem()

        # 租房名称
        name = sel.xpath("//div[@class='title']/h1[@class='main']/text()")[0]
        item["name"] = name
        # item["name"] = name.split(" ")[0]

        # 租房价格
        price = sel.xpath("//div[@class='price ']/span/text()")
        unit = sel.xpath("//div[@class='price ']/span[@class='unit']/span/text()")
        item["price"] = price[0].strip() + unit[0]

        # 租房面积
        # /html/body/div[4]/div[2]/div[2]/div[2]/p[1]
        area = sel.xpath("//div[@class='zf-room']/p[@class='lf'][1]/text()")
        item['area'] = area[0]

        # 租房户型
        type = sel.xpath("//div[@class='zf-room']/p[@class='lf'][2]/text()")
        item['type'] = type[0].strip()

        # 租房楼层
        floor = sel.xpath("//div[@class='zf-room']/p[@class='lf'][3]/text()")
        item['floor'] = floor[0]

        # 租房朝向
        direction = sel.xpath("//div[@class='zf-room']/p[@class='lf'][4]/text()")
        item['direction'] = direction[0]

        # 附近地铁
        subway = sel.xpath("//div[@class='zf-room']/p[5]/text()")
        item['subway'] = subway[0]

        # 租房小区
        community = sel.xpath("//div[@class='zf-room']/p[6]/a/text()")
        item['community'] = community[0] + '-' + community[1]

        # 租房位置
        # /html/body/div[4]/div[2]/div[2]/div[2]/p[7]
        location = sel.xpath("//div[@class='zf-room']/p[7]/a/text()")
        item['location'] = location[0] + location[1]

        # 发布时间
        time = sel.xpath("//div[@class='zf-room']/p[@class='lf'][5]/text()")
        item['time'] = time[0]

        # 租房url
        item['url'] = url

        yield item

