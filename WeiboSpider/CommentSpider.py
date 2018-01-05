# -*- coding: UTF-8 -*-

import re
import requests
import sys
import traceback
from lxml import etree
import pymongo
import random
import time as systime

class WeiboComment:
<<<<<<< HEAD
    cookie = {"Cookie": "_T_WM=00dab9533b7fcab9969b54488c0007b9;"
                        " SUB=_2A253Sdw7DeRhGeNH7FIX-CvNzT-IHXVUteRzrDV6PUJbkdBeLUjVkW1NSpOgtXzOQWn7ZuVWQkeAdyOr-zkU85CW; "
                        "SUHB=0bt8fR1QeGrxXH; "
                        "SCF=AoTYxXIQ97QY0k1CNkRjEicPIWzzavue932JWj5nxoV-o6KV6-NAvFJl064DP5-NvxOauzv2RhraTB3p5WqgVc0.;"
                        " SSOLoginState=1515039851"}  # 将your cookie替换成自己的cookie

=======
    cookie = {"Cookie": "Your Cookies"}  # 将your cookie替换成自己的cookie
>>>>>>> 6f4f11a2e9fa7d5293376703bea953040ecf990b

    # WeiboComment类初始化
    def __init__(self, user_id, comment_id, publish_time, filter=0):
        self.user_id = user_id  # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
        self.comment_id = comment_id    # 微博代号
        self.publish_time = publish_time  # 微博发布时间

        # 建立评论数据库
        dbClient = pymongo.MongoClient(host='localhost', port=27017)
        Comment = dbClient[str(self.user_id) + '--微博评论']
        self.WeiboCommentData = Comment[str(publish_time)]
        if self.WeiboCommentData.find():
            self.WeiboCommentData.remove({})

    # 获取微博下面的评论
    def get_weibo_comment(self):
        try:
            url = "https://weibo.cn/comment/%s?uid=%d&rl=0&page=1" % (
                self.comment_id, self.user_id)      # 所有评论url2

            # url = "https://weibo.cn/comment/hot/%s?rl=1&page=1" % (
            #     self.comment_id)     # 热门评论url
            html = requests.get(url, cookies = self.cookie).content
            selector = etree.HTML(html)

            if selector.xpath("//input[@name='mp']") == []:
                page_num = 1
            else:
                page_num = (int)(selector.xpath(
                    "//input[@name='mp']")[0].attrib["value"])
            pattern = r"\d+\.?\d*"
            for page in range(1, page_num+1):
                print("正在爬取%s/%s页评论" % (page, page_num))
                url2 = "https://weibo.cn/comment/%s?uid=%d&rl=0&page=%d" % (
                self.comment_id, self.user_id, page)    # 所有评论url2

                # url2 = "https://weibo.cn/comment/hot/%s?rl=1&page=%d" % (
                # self.comment_id, page)    # 热门评论url2
                html2 = requests.get(url2, cookies = self.cookie).content
                selector2 = etree.HTML(html2)
                info = selector2.xpath("//div[@class='c']")

                # 判断该页是否有评论，如果爬取的是热门评论，条件改为 > 1 即可
                if len(info) > 3:

                    # 跳过第一页的三条热门，如果爬取的是热门评论，直接将 begin_page 换成1即可
                    if page == 1:
                        begin_page = 5
                    else:
                        begin_page = 2

                    for i in range(begin_page, len(info)):

                        # 自动跳过中间的更多热门
                        if len(info[i]) < 2:
                            continue

                        # 用户ID及用户名
                        id_info = info[i].xpath("a/@href")
                        name_info = info[i].xpath("a[@href]/text()")
                        _id = id_info[0]
                        _name = name_info[0]

                        # 评论内容
                        comment_info = info[i].xpath("span[@class='ctt']")
                        try:
                            _comment = comment_info[0].xpath("string(.)").encode(
                            sys.stdout.encoding, "ignore").decode(
                            sys.stdout.encoding)
                        except Exception as e:
                            print ("Error: ", e)

                        # 发布时的状态，包括发布时间和发布设备
                        publish_info = info[i].xpath("span[@class='ct']")
                        try:
                            publish_info = publish_info[0].xpath("string(.)").encode(
                            sys.stdout.encoding, "ignore").decode(
                            sys.stdout.encoding)
                        except Exception as e:
                            print ("Error: ", e)

                        # 给手机型号大致分类
                        _device = publish_info.split(u'来自')[1]
                        device_list = ['Android', 'iPhone', '网页' ,'微博']
                        for device in device_list:
                            if device in _device:
                                _device = device
                                break

                        # 点赞数
                        like_info = info[i].xpath("span[@class='cc']")
                        try:
                            like_info = like_info[0].xpath("a/text()")[0]
                            str_like = re.findall(pattern, like_info, re.M)
                            _like = int(str_like[0])
                        except Exception as e:
                            # print ("第%s条微博点赞数Error: %s" %(self.weibo_num2, e))
                            _like = 0

                        # 将数据存储到数据库
                        data = {
                            '评论人ID':_id,
                            '评论人昵称':_name,
                            '评论内容':_comment,
                            '设备':_device,
                            '点赞数':_like
                        }

                        self.WeiboCommentData.insert_one(data)
                        # print("微博评论：" + _comment)
                if (page % 50 ==0):
                    systime.sleep(5 + float(random.randint(1, 10)) / 20)
                systime.sleep(0.5 + float(random.randint(1, 10)) / 20)
        except Exception as e:
            print ("Error: ", e, " 怕是老哥爬的太快，被封了哟，赶紧提高爬虫姿势水平")
            traceback.print_exc()

    def start(self):
        try:
            self.get_weibo_comment()
        except Exception as e:
            print ("Error: ", e)

def main():
<<<<<<< HEAD
    user_id = 5992855888  # 可以改成任意合法的用户id（爬虫的微博id除外）
    filter = 0  # 值为0表示爬取全部微博（原创微博+转发微博），值为1表示只爬取原创微博
    comment_id = 'FCVnRgBL'
    publish_time ='2018-01-05 10:04'
    try:
        Comment = WeiboComment(user_id, comment_id, publish_time, filter)
        Comment.start()
    except Exception as e:
        print ("Error: ", e)
        traceback.print_exc()
=======
    user_id = 5992855888      # 可以改成任意合法的用户id（爬虫的微博id除外）
    filter = 0      # 值为0表示爬取全部微博（原创微博+转发微博），值为1表示只爬取原创微博
    # comment_id = 'CrF4s7ecG'    # 你要爬取的微博的ID，可以通过前面爬取微博的时候得到
    # publish_time ='2015-07-18 12:06'    # 发布时间也可以通过前面爬取微博的时候得到
    f = open("id.txt", 'r')
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')

        comment_id, publish_time = line[:9], line[11:27]
        print(comment_id, publish_time)
        try:
            Comment = WeiboComment(user_id, comment_id, publish_time, filter)
            Comment.start()
        except Exception as e:
            print ("Error: ", e)
            traceback.print_exc()
        systime.sleep(2 + float(random.randint(1, 10)) / 20)
>>>>>>> 6f4f11a2e9fa7d5293376703bea953040ecf990b

if __name__ == "__main__":
    main()
