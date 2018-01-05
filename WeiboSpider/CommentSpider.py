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
    cookie = {"Cookie": "_T_WM=00dab9533b7fcab9969b54488c0007b9;"
                        " SUB=_2A253Sdw7DeRhGeNH7FIX-CvNzT-IHXVUteRzrDV6PUJbkdBeLUjVkW1NSpOgtXzOQWn7ZuVWQkeAdyOr-zkU85CW; "
                        "SUHB=0bt8fR1QeGrxXH; "
                        "SCF=AoTYxXIQ97QY0k1CNkRjEicPIWzzavue932JWj5nxoV-o6KV6-NAvFJl064DP5-NvxOauzv2RhraTB3p5WqgVc0.;"
                        " SSOLoginState=1515039851"}  # 将your cookie替换成自己的cookie


    # WeiboComment类初始化
    def __init__(self, user_id, comment_id, publish_time, filter=0):
        self.user_id = user_id  # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
        self.comment_id = comment_id    # 微博代号
        self.publish_time = publish_time  # 微博发布时间

        # 建立评论数据库
        dbClient = pymongo.MongoClient(host='localhost', port=27017)
        Comment = dbClient[str(self.user_id) + 'Comment']
        self.WeiboCommentData = Comment[str(user_id) + '_' + str(publish_time)]
        if self.WeiboCommentData.find():
            self.WeiboCommentData.remove({})

    # 获取微博下面的评论
    def get_weibo_comment(self):
        try:
            # url = "https://weibo.cn/comment/%s?uid=%d&rl=0&page=1" % (
            #     self.comment_id, self.user_id)
            url = "https://weibo.cn/comment/hot/%s?rl=1&page=1" % (
                self.comment_id)     # 热门评论url
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
                # url2 = "https://weibo.cn/comment/%s?uid=%d&rl=0&page=%d" % (
                # self.comment_id, self.user_id, page)
                url2 = "https://weibo.cn/comment/hot/%s?rl=1&page=%d" % (
                self.comment_id, page)
                html2 = requests.get(url2, cookies = self.cookie).content
                selector2 = etree.HTML(html2)
                info = selector2.xpath("//div[@class='c']")
                if len(info) > 1:
                    for i in range(1, len(info)):
                        # 账号名
                        str_id = info[i].xpath("a/@href")
                        str_name = info[i].xpath("a[@href]/text()")
                        str_id = str_id[0]
                        str_name = str_name[0]

                        # 评论内容
                        str_t = info[i].xpath("span[@class='ctt']")
                        try:
                            comment_content = str_t[0].xpath("string(.)").encode(
                            sys.stdout.encoding, "ignore").decode(
                            sys.stdout.encoding)
                        except Exception as e:
                            print ("Error: ", e)

                        # 手机型号
                        str_time = info[i].xpath("span[@class='ct']")
                        str_time = str_time[0].xpath("string(.)").encode(
                            sys.stdout.encoding, "ignore").decode(
                            sys.stdout.encoding)

                        # 给手机型号大致分类
                        str_model = str_time.split(u'来自')[1]
                        model_list = ['Android', 'iPhone', '网页' ,'微博']
                        for model in model_list:
                            if model in str_model:
                                str_model = model
                                break

                        # 点赞数
                        info_zan = info[i].xpath("span[@class='cc']")
                        try:
                            str_zan = info_zan[0].xpath("a/text()")[0]
                            guid = re.findall(pattern, str_zan, re.M)
                            up_num = int(guid[0])
                        except Exception as e:
                            # print ("第%s条微博点赞数Error: %s" %(self.weibo_num2, e))
                            up_num = 0
                        # 数据库
                        data = {
                            '评论人ID':str_id,
                            '评论人昵称':str_name,
                            '评论内容':comment_content,
                            '设备':str_model,
                            '点赞数':up_num
                        }

                        self.WeiboCommentData.insert_one(data)
                        # print("微博评论：" + comment_content)

                systime.sleep(0.3 + float(random.randint(1, 10)) / 40)
        except Exception as e:
            print ("Error: ", e)
            traceback.print_exc()

    def start(self):
        try:
            self.get_weibo_comment()
        except Exception as e:
            print ("Error: ", e)

def main():
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

if __name__ == "__main__":
    main()
