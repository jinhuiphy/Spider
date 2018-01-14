# -*- coding:utf-8 -*-
import os


user_id = 1214435497

valuePath = "EmotionValue/" + str(user_id) + '_emotion_value/' + str(user_id) + '_emotion_Total.txt'
commentPath = "WeiboComment/" + str(user_id) + '_comment/' + str(user_id) + '_comment_Total.txt'

startPath = "NegPos/" + str(user_id) + "_result/"
if not os.path.exists(startPath):
    os.makedirs(startPath)

posPath = startPath + str(user_id) + '_pos_result.txt'
negPath = startPath + str(user_id) + '_neg_result.txt'

valueFile = open(valuePath, 'r', encoding='utf-8')
commentFile = open(commentPath, 'r', encoding='utf-8')

posFile = open(posPath, 'w', encoding='utf-8')
negFile = open(negPath, 'w', encoding='utf-8')

valueLines = valueFile.readlines()
commentLines = commentFile.readlines()

for i in range(len(valueLines)):
    if i % 1000 == 0:
        print("正在写入第%s千行" % (i/1000))
    if float(valueLines[i]) >= 0.5:
        posFile.write(valueLines[i].strip('\n') + '\t' + commentLines[i])
    else:
        negFile.write(valueLines[i].strip('\n') + '\t' + commentLines[i])
print("Finished")
