# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class LianjiazufangPipeline(object):

    def  __init__(self):
        dbClient = pymongo.MongoClient(host='localhost', port=27017)
        LianJia = dbClient['LianJiaZuFang']
        count = 1
        city = input("请输入城市名称，如NanJing、ShangHai：")
        self.ZuFang = LianJia[city + 'ZuFang']
        if self.ZuFang.find({}).count():
            confirm = input("该数据库已存在，确认要覆盖数据库%s请输入yes，其他输入默认建立副本" % (city + 'ZuFang'))
            if confirm == 'yes':
                print("正在清空数据库")
                self.ZuFang.remove({})
            else:
                print("正在建立副本")
                self.ZuFang = LianJia[city + 'ZuFang' + '副本--' + str(count)]
                while self.ZuFang.find({}).count():
                    print("建立副本中正在尝试第%s次" % count)
                    count += 1
                    self.ZuFang = LianJia[city + 'ZuFang' + '副本--' + str(count)]

            # self.LouPan.remove({})

    def process_item(self, item, spider):
        data =dict(item)
        self.ZuFang.insert_one(data)

