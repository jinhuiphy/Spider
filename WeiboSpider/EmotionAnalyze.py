import matplotlib.pyplot as plt
import numpy as np
from snownlp import SnowNLP
import datetime


def getData(commentPath, emotionPath):
    """使用snowlp来分析每一条评论的情感值"""
    readFile = open(commentPath, 'r', encoding='utf-8')  # 评论的txt文件
    resultFile = open(emotionPath, 'w', encoding='utf-8')  # 存放情感值的txt文件

    lines = readFile.readlines()

    start = 0
    end = len(lines)

    total = end // 1000

    start_time = datetime.datetime.now()
    for i in range(start, end):

        time = i % 1000
        if time == 0:
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
    print("画图中，请稍后")
    sentimentsList = []
    # emotionPath = "EmotionValue/" + str(user_id) + '_emotion_Part' + str(part) + '.txt'
    readFile = open(emotionPath, 'r', encoding='utf-8')
    lines = readFile.readlines()
    for line in lines:
        # value = line.split('\t')[1]
        value = line
        sentimentsList.append(float(value))

    plt.hist(sentimentsList, bins=np.arange(0, 1, 0.01), color='g', edgecolor='b', normed=True)  # , cumulative=True
    plt.xlabel('Emotion Value')
    plt.ylabel('Probability')
    plt.title('Emotional analysis statistics histogram')
    # plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    plt.grid(True)
    plt.show()
    print("作图完毕")


def main():
    user_id = 1214435497
    part = 23
    print("当前进程Part%s" % part)

    commentPath = "WeiboComment/" + str(user_id) + '_comment_Part' + str(part) + '.txt'
    emotionPath = "EmotionValue/" + str(user_id) + '_emotion_Part' + str(part) + '.txt'
    # commentPath = "WeiboComment/" + str(user_id) + '_comment_Total.txt'
    # emotionPath = "EmotionValue/" + str(user_id) + '_emotion_Total.txt'
    getData(commentPath, emotionPath)
    # Draw(user_id, emotionPath)


if __name__ == "__main__":
    main()
