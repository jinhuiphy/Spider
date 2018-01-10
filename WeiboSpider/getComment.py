from Weibo import Weibo
import time
import random
import traceback
import cookies
import pymongo

def save_as_txt(db, dataPath):
    '''将数据库里的东西保存为文本'''
    with open(dataPath, 'w', encoding='utf-8') as f:
        for i in db.find({})[1::]:
            f.write(i["微博ID"] + '\t' + i["发布时间"] + '\n')

def getID(user_id, idPath):
    '''获取微博ID'''
    dbClient = pymongo.MongoClient(host='localhost', port=27017)

    Weibo = dbClient["Weibo"]
    WeiboID = Weibo[str(user_id)]

    save_as_txt(WeiboID, idPath)

def main():
    user_id = 5992855888      # 可以改成任意合法的用户id（爬虫的微博id除外）
    filter = 0      # 值为0表示爬取全部微博（原创微博+转发微博），值为1表示只爬取原创微博
    # comment_id = 'CrF4s7ecG'    # 你要爬取的微博的ID，可以通过前面爬取微博的时候得到
    # publish_time ='2015-07-18 12:06'    # 发布时间也可以通过前面爬取微博的时候得到


    # 读取微博的所有ID信息，如果ID.txt不存在，则自动创建
    idPath = "WeiboID/" + str(user_id) + '_id.txt'
    try:
        file = open(idPath, 'r')
        lines = file.readlines()
    except:
        print("ID文件不存在，将自动创建")
        getID(user_id, idPath)
        file = open(idPath, 'r')
        lines = file.readlines()

    last_start = 225      # 记录上一次爬到哪里，继续爬的话只需要将start改为last_start的值即可
    start = 225
    end = len(lines)
    for i in range(start, end):
        print("正在爬取第%d/%d条微博" % (i+1, end+1))
        line = lines[i].strip('\n')
        weibo_id, publish_time = line[:9], line[10:27]
        print(weibo_id, publish_time)
        try:
            if i % 20 == 0:
                time.sleep(20 + float(random.randint(1, 10)) / 20)  #爬取20条微博停止5s左右
            Comment = Weibo(user_id, weibo_id, publish_time, filter)
            Comment.auto_get()
        except Exception as e:
            cookie = cookies[1]
            print("Cookie 已切换")
            print ("Error: ", e)
            traceback.print_exc()
        # 每一条微博加个2s的延迟
        time.sleep(3 + float(random.randint(1, 10)) / 20)

if __name__ == "__main__":
    main()
