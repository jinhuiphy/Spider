import pymongo

def save_as_txt(db, dataPath):
    with open(dataPath, 'a', encoding='utf-8') as f:
        for i in db.find({}):    #"author": u"机器猫"
            f.write(i["评论内容"] + '\n')

def main():
    # 建立评论数据库
    user_id = 5992855888
    dataPath = r'comment.txt'
    dbClient = pymongo.MongoClient(host='localhost', port=27017)
    Comment = dbClient[str(user_id) + '--微博评论']
    collection_list = Comment.collection_names()
    file = open(dataPath, 'w', encoding='utf-8')

    for i in range(len(collection_list)):
        # print(collection_list[i])
        print("正在保存第%s条微博评论" % (i+1))
        db = Comment[collection_list[i]]
        for comment in db.find({}):
            file.write(comment["评论内容"] + '\n')
    print("%s条微博评论已保存" % (len(collection_list) + 1))

if __name__ == "__main__":
    main()
