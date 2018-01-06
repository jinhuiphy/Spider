import matplotlib.pyplot as plt
import numpy as np
from snownlp import SnowNLP

def getData():
    '''使用snowlp来分析每一条评论的情感值'''
    readFile = open(r'comment.txt','r',encoding='utf-8') # 评论的txt文件
    resultFile = open(r'data.txt','w',encoding='utf-8') # 存放情感值的txt文件

    lines = readFile.readlines()

    start= 0
    end = len(lines)

    for i in range(start, end):
        print("正在分析第%s/%s条评论" % (i+1, end+1))
        snow = SnowNLP(lines[i])
        data = snow.sentiments
        resultFile.write(str(data)+'\n')

    readFile.close()
    resultFile.close()

def Draw():
    '''将情感分析的数值以hist的形式画出来'''
    sentimentsList = []
    readFile = open(r'data.txt','r',encoding='utf-8')
    lines = readFile.readlines()
    for line in lines:
        sentimentsList.append(float(line))

    plt.hist(sentimentsList, bins = np.arange(0, 1, 0.01), color = 'g', edgecolor = 'b')
    plt.xlabel('Emotion Value')
    plt.ylabel('Probability')
    plt.title('Emotional analysis statistics histogram')
    plt.axis([0, 1, 0, 500])
    plt.grid(True)
    plt.show()

def main():
    # getData()
    Draw()

if __name__ == "__main__":
    main()

