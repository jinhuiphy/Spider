import requests
from lxml import etree




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
name=[]
data=[]
name=selector.xpath("//dd//@title") #公交线路名称
data=selector.xpath("//dd//@href") #线路具体网址
a=len(data)
b=len(name)
f=open('stations.txt','w',encoding='utf-8')
for i in range(b):
    f.write(name[i]+'\n')
    stations=station(data[i])
    for Station in stations:
        f.write('南京'+Station+'(公交站）'+'\n') #精细地址，为了便于后面调用百度的api


