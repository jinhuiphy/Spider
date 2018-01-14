import pymongo
import os

def save_as_txt(db, dataPath):
    with open(dataPath, 'w', encoding='utf-8') as f:
        for i in db.find({})[1::]:    # "author": u"机器猫"
            f.write(i["微博ID"] + '\t' + i["发布时间"] + '\n')


def main():
    """该函数主要将同一用户所有微博的所有评论都保存为txt，便于后面做情感分析"""
    user_id = 3591355593
    real_id = 1214435497
    part = 23
    print("正在保存第%s部分" % part)
    startPath = 'WeiboComment/' + str(user_id) +'_comment/'
    if not os.path.exists(startPath):
        os.makedirs(startPath)

    commentPath = startPath + str(user_id) + '_emotion_Part' + str(part) + '.txt'
    file = open(commentPath, 'w', encoding='utf-8')

    dbClient = pymongo.MongoClient(host='localhost', port=27017)
    Comment = dbClient[str(user_id) + "--微博评论--Part" + str(part)]
    collection_list = Comment.collection_names()

    for i in range(len(collection_list)):
        # print(collection_list[i])
        print("正在保存第%s条微博评论" % (i+1))
        db = Comment[collection_list[i]]
        for comment in db.find({}):
            file.write(comment["评论内容"] + '\n')      # collection_list[i] + '\t' +
    print("%s条微博评论已保存" % (len(collection_list) + 1))


if __name__ == "__main__":
    main()
