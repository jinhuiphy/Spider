import requests
from lxml import etree
import json

def station(url):
    stations=[] #以列表的形式存储公交站点名称
    url0=url #线路具体站点的url
    html = requests.get(url0).content #get html
    html = str(html, 'utf-8') #指定utf-8编码
    selector = etree.HTML(html)
    stations=selector.xpath("//div[@class='publicBox buslist']//li/a/@title") #得到公交站点名称
    return stations

url='http://bus.mapbar.com/nanjing/xianlu' #从图吧得到的所有路线
html=requests.get(url).content #get html
html=str(html,'utf-8') #指定utf-8编码
selector = etree.HTML(html)
line=open('line.json','w',encoding='utf-8')
name=[]
data=[]
name=selector.xpath("//dd//@title") #公交线路名称
data=selector.xpath("//dd//@href") #线路具体网址
a=len(data)
b=len(name)
f=open('stations.json','w',encoding='utf-8')
for i in range(b):
    linedata={}
    linedata['name']=name[i]
    stations=station(data[i])
    m=len(stations)
    for k in range(m):
        linedata['station'+str(k)]=stations[k]
    json.dump(linedata,line, ensure_ascii=False)
    line.write('\n')

