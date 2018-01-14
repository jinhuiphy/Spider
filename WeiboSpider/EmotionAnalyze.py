import matplotlib.pyplot as plt
import numpy as np
from snownlp import SnowNLP
import datetime
import os

def getData(commentPath, emotionPath):
    """使用snowlp来分析每一条评论的情感值"""
    readFile = open(commentPath, 'r', encoding='utf-8')  # 评论的txt文件
    resultFile = open(emotionPath, 'w', encoding='utf-8')  # 存放情感值的txt文件

    lines = readFile.readlines()

    start = 0
    end = len(lines)
    total = int(end // 1000)

    start_time = datetime.datetime.now()
    for i in range(start, end):
        if i % 1000 == 0:
            end_time = datetime.datetime.now()
            print("正在分析第%s/%s千条评论" % (i//1000 + 1, total))
            print("耗时%s" %(end_time - start_time))
        # print("正在分析第%s/%s条评论" % (i + 1, end + 1))
        # time = lines[i].split('\t')[0]
        # comment = lines[i].split('\t')[1]
        comment = lines[i]
        snow = SnowNLP(comment)
        data = snow.sentiments
        resultFile.write(str(data) + '\n')      # time + '\t' +

    print("评论分析完毕")

    readFile.close()
    resultFile.close()


def Draw(user_id, emotionPath):
    """将情感分析的数值以hist的形式画出来"""

    sentimentsList = []

    readFile = open(emotionPath, 'r', encoding='utf-8')
    lines = readFile.readlines()

    print("正在读取%s条数据" % len(lines))

    for line in lines:
        # value = line.split('\t')[1]
        value = line
        # if float(value) == 1.0:
        #     count += 1
        sentimentsList.append(float(value))
    print("画图中，请稍后")
    plt.hist(sentimentsList, bins=np.arange(0, 1.01, 0.2), color='g', edgecolor='k')  # , cumulative=True, normed=True
    plt.xlabel('Emotion Value')
    # plt.ylabel('Probability')
    plt.ylabel('Frequency')
    plt.title('Emotional analysis statistics histogram')
    plt.grid(True)
    plt.show()
    print("作图完毕")


def main():
    user_id = 1214435497
    part = 23
    # print("当前进程Part%s" % part)

    # 如果文件夹不存在就自动创建
    startPath = "EmotionValue/" + str(user_id) + '_emotion_value/'
    if not os.path.exists(startPath):
        os.makedirs(startPath)

    # 文件路径，如果part取0，代表的是总的文件
    if part ==  0:
        commentPath = "WeiboComment/" + str(user_id) + '_comment/' + str(user_id) + '_comment_Total.txt'
        emotionPath = startPath + str(user_id) + '_emotion_Total.txt'
    else:
        commentPath = "WeiboComment/" + str(user_id) + '_comment/' + str(user_id) + '_comment_Part' + str(part) + '.txt'
        emotionPath = startPath + str(user_id) + '_emotion_Part' + str(part) + '.txt'

    getData(commentPath, emotionPath)
    Draw(user_id, emotionPath)


if __name__ == "__main__":
    main()
