from snownlp import SnowNLP
f=open(r'comment.txt','r',encoding='utf-8') #评论的txt文件
F=open(r'data.txt','w',encoding='utf-8') #存放情感值的txt文件
line=f.readline()
i=0
while line:
    print(i)
    s1=SnowNLP(line)
    data=s1.sentiments
    F.writelines(str(data)+'\n')
    line=f.readline()
    i=i+1
f.close()
F.close()