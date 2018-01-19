# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class LianjialoupanPipeline(object):

    def  __init__(self):
        dbClient = pymongo.MongoClient(host='localhost', port=27017)
        LianJia = dbClient['LianJia']
        count = 1
        city = input("请输入城市名称，如NanJing、ShangHai：")
        self.LouPan = LianJia[city + 'LouPan']
        if self.LouPan.find({}).count():
            confirm = input("确认要覆盖数据库%s请输入yes，其他输入默认建立副本" % (city + 'LouPan'))
            if confirm == 'yes':
                print("正在清空数据库")
                self.LouPan.remove({})
            else:
                print("正在建立副本")
                self.LouPan = LianJia[city + 'LouPan' + '副本--' + str(count)]
                while self.LouPan.find({}).count():
                    print("建立副本中正在尝试第%s次" % count)
                    count += 1
                    self.LouPan = LianJia[city + 'LouPan' + '副本--' + str(count)]


    def process_item(self, item, spider):
        data =dict(item)
        self.LouPan.insert_one(data)
