import urllib.request
import urllib
import json
from urllib.request import urlopen, quote
left_bottom=[118.761207,32.005045]#地点
right_top=[118.841268,32.053]#南京中山植物园
part_n=4

url0='http://api.map.baidu.com/place/v2/search?'
x_item = (right_top[0]-left_bottom[0])/part_n
y_item = (right_top[1]-left_bottom[1])/part_n
query = '公交站'
station=quote(query)
jsondata=open('jsondata.txt','w',encoding='utf-8')
ak=''#填写你的密钥
BusStation=open('BusStation.txt','w',encoding='utf-8')
address=open('address.txt','w',encoding='utf-8')
n=0
f=open('data0.txt','w',encoding='utf-8')
for i in range(part_n):
    for j in range(part_n):
        left_bottom_part = [left_bottom[0]+i*x_item,left_bottom[1]+j*y_item] # 切片的左下角坐标
        right_top_part = [right_top[0]+i*x_item,right_top[1]+j*y_item] # 切片的右上角坐标
        for k in range(20):
            url = url0 + 'query=' + station + '&page_size=20&page_num=' + str(k) + '&scope=1&bounds=' + str(left_bottom_part[1]) + ',' + str(left_bottom_part[0]) + ','+str(right_top_part[1]) + ',' + str(right_top_part[0]) + '&output=json&ak=' + ak
            data = urllib.request.urlopen(url)
            hjson = json.loads(data.read())
            if hjson['message'] == 'ok':
                results = hjson['results']
                for m in range(len(results)):# 提取返回的结果
                    f.write(str(results[m]['location']['lng'])+'\t'+str(results[m]['location']['lat'])+'\n')
                    jsondata.write(str(results[m])+'\n')
                    BusStation.write(results[m]['name']+'\n')
                    address.write(results[m]['address']+'\n')
        n=n+1
        print('第', str(n), '个切片入库成功')


