#-*- coding:utf-8 -*-
import pymongo
import CheckLegal

def save_as_txt(db, dataPath):
    with open(dataPath, 'w', encoding='utf-8') as f:
        for i in db.find({}):    #"author": u"机器猫"
            f.write(i["content"])

def main():
    # 初始化参数
    questionID = '65641135'
    dbClient = pymongo.MongoClient(host='localhost', port=27017)
    Zhihu = dbClient['Zhihu']
    ZhihuData = Zhihu[questionID + '_copy']
    dataPath = r'Zhihu.txt'
    fileRead = open(r'Zhihu.txt', 'r', encoding='utf-8')
    fileWrite = open(r'result.txt', 'w', encoding='utf-8')
    # 将数据库内的content读取出来并存为txt
    save_as_txt(ZhihuData, dataPath)
    # 处理txt文本当中的信息，只保留汉字及一些基本的标点
    while True:
        line = fileRead.readline()
        if len(line) == 0:
            break
        strBuffer = str(line)
        string = ""
        for oneWord in strBuffer:
            if CheckLegal.is_chinese(oneWord) or CheckLegal.is_punc(oneWord):
                string += oneWord
        fileWrite.write(string)
        fileWrite.write('\n')
    fileRead.close()
    fileWrite.close()

if __name__ == '__main__':
    main()

