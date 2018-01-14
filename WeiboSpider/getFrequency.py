# -*- coding:utf-8 -*-
import os
import jieba
from collections import Counter


def main():
    user_id = 1214435497     # 可以改成任意合法的用户id（爬虫的微博id除外）
    part = 22
    startPath = 'Frequency/' + str(user_id) + '_frequency/'
    if not os.path.exists(startPath):
        os.makedirs(startPath)
    # os.makedirs('trequency/' + str(user_id) + '_frequency/')
    commentPath = "WeiboComment/" + str(user_id) + '_comment/' + str(user_id) + '_comment_Part' + str(part) + '.txt'
    frequencyPath = startPath + str(user_id) + '_frequency_Part' + str(part) + '.txt'
    # commentPath = "WeiboComment/" + str(user_id) + '_comment/' + str(user_id) + '_comment_Total.txt'
    # frequencyPath = startPath + str(user_id) + '_frequency_Total.txt'
    getData(commentPath, frequencyPath)

def getData(commentPath, frequencyPath):
    readFile = open(commentPath, 'r', encoding='utf-8')  # 评论的txt文件
    resultFile = open(frequencyPath, 'w', encoding='utf-8')  # 存放情感值的txt文件

    data = jieba.cut(readFile.read())
    data = dict(Counter(data).most_common(2000))
    # print(Counter(data).most_common(5))

    for w,f in data.items():
        resultFile.write("%s\t%d\n" % (w, f))
    print("获取词频结束")


if __name__ == "__main__":
    main()

