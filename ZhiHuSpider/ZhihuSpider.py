from zhihu_oauth import ZhihuClient
from zhihu_oauth.exception import NeedCaptchaException
import pymongo
import time
import random
# 账户信息以及问题ID
account = 'account'
passwd = 'passwd'
questionID = 264747923
# 建立数据库
dbClient = pymongo.MongoClient(host='localhost', port=27017)
Zhihu = dbClient['Zhihu']
ZhihuData = Zhihu[str(questionID)]
if ZhihuData.find():
        ZhihuData.remove({})
# 登陆知乎账号
client = ZhihuClient()
try:
    client.login(account, passwd)
except NeedCaptchaException:
    # 保存验证码并提示输入，重新登录
    with open('a.gif', 'wb') as f:
        f.write(client.get_captcha())
    captcha = input('please input captcha:')
    client.login(account, passwd, captcha)
# 创建问题对象
question = client.question(questionID)
# 读取问题下所有的回答并保存起来
print(question.title)
count = 0
for answer in question.answers:
    count+=1
    try:
        data = {
            'title':question.title,
            'author':answer.author.name,
            'description':answer.author.description,
            'content':answer.content,
            'voteup':answer.voteup_count,
            'thanks':answer.thanks_count
        }
        print("正在保存第%s个回答" %count)
        ZhihuData.insert_one(data)
        time.sleep(0.5 + float(random.randint(1, 10)) / 20)
    except:
        print("第%s个回答跳过" %count)
