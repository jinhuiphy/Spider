# -*- coding: UTF-8 -*-

import re
import requests
import sys
import traceback
from lxml import etree
import pymongo
import random
import time as systime
from agent import agents
from cookies import cookies

class Weibo:
    '''将微博单独抽象为一个类，该类主要用来爬取单条微博的评论数据'''

    # Weibo类初始化
    def __init__(self, user_id, weibo_id, publish_time, start_page, filter=0):
        self.user_id = user_id  # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
        self.comment_id = weibo_id    # 微博代号
        self.publish_time = publish_time  # 微博发布时间
        self.start_page = start_page    # 爬取的评论起始页

        # 建立评论数据库
        dbClient = pymongo.MongoClient(host='localhost', port=27017)
        Comment = dbClient[str(self.user_id) + '--微博评论']
        self.WeiboCommentData = Comment[str(publish_time)]
        if self.start_page == 1:
            if self.WeiboCommentData.find():
                print("正在清空数据库")
                self.WeiboCommentData.remove({})
        else:
            print("上次爬到第%s页,正在续爬" % self.start_page)

        # 随机选取浏览器
        UA = random.choice(agents)
        self.headers = {'User-Agent': UA}

        # 设置cookies
        # self.cookie = random.choice(cookies)
        self.cookie  = cookies[0]

    # 获取微博下面的评论
    def get_save_comment(self):
        try:
            url = "https://weibo.cn/comment/%s?uid=%d&rl=0&page=1" % (
                self.comment_id, self.user_id)      # 所有评论url2

            # url = "https://weibo.cn/comment/hot/%s?rl=1&page=1" % (
            #     self.comment_id)     # 热门评论url

            html = requests.get(url, cookies = self.cookie, headers=self.headers).content
            selector = etree.HTML(html)

            if selector.xpath("//input[@name='mp']") == []:
                page_num = 1
            else:
                page_num = (int)(selector.xpath(
                    "//input[@name='mp']")[0].attrib["value"])
            print(page_num)
            pattern = r"\d+\.?\d*"

            # 用来记录没有评论的页数出现的次数，如果连续5页都没有评论，则结束程序
            count = 0

            for page in range(self.start_page, page_num+1):
                # 每爬30页就切换个cookie并随机切换浏览器
                if (page) % 30 == 0:

                    UA = random.choice(agents)
                    self.headers = {'User-Agent': UA}

                    num = page / 30

                    choice = int(num % len(cookies))
                    self.cookie = cookies[choice]
                    print("Cookie已切换为第%s个" % (choice + 1))

                url2 = "https://weibo.cn/comment/%s?uid=%d&rl=0&page=%d" % (
                self.comment_id, self.user_id, page)    # 所有评论url2

                # url2 = "https://weibo.cn/comment/hot/%s?rl=1&page=%d" % (
                # self.comment_id, page)    # 热门评论url2
                html2 = requests.get(url2, cookies = self.cookie, headers = self.headers).content
                selector2 = etree.HTML(html2)
                info = selector2.xpath("//div[@class='c']")

                # 判断该页是否有评论，如果爬取的是热门评论，条件改为 > 1 即可
                if len(info) > 3:
                    print("正在爬取%s/%s页评论" % (page, page_num))

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
                            print ("爬取评论内容时出错：", e)

                        # 发布时的状态，包括发布时间和发布设备
                        publish_info = info[i].xpath("span[@class='ct']")
                        try:
                            publish_info = publish_info[0].xpath("string(.)").encode(
                            sys.stdout.encoding, "ignore").decode(
                            sys.stdout.encoding)
                        except Exception as e:
                            print ("爬取发布状态时出错: ", e)

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

                        # 保证count最小为0
                        if count > 0:
                            count -= 1

                else:
                    print("该页无评论，已跳过")
                    count += 1
                    if count == 5:
                        print("已经连续5页没有评论，该条微博自动结束")
                        break

                # 评论的每一页加个0.1s的延迟
                systime.sleep(0.1 + float(random.randint(1, 5)) / 20)
        except Exception as e:
            print ("Error: ", e, " 怕是老哥爬的太快，被封了哟，赶紧提高爬虫姿势水平")
            traceback.print_exc()

    def auto_get(self):
        try:
            self.get_save_comment()
        except Exception as e:
            print ("Error: ", e)


