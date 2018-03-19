import json
import urllib
import math
import urllib.request
from urllib.request import urlopen, quote

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 偏心率平方

def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'
    ak = '' #这里填写百度地图密钥
    add = quote(address) #由于本文城市变量为中文，为防止乱码，先用quote进行编码
    uri = url + '?' + 'address=' + add  + '&output=' + output + '&ak=' + ak
    req = urlopen(uri)
    res = req.read().decode() #将其他编码的字符串解码成unicode
    temp = json.loads(res) #对json数据进行解析
    return temp

def bd09_to_gcj02(bd_lon, bd_lat):
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)
    百度——>谷歌、高德
    :param bd_lat:百度坐标纬度
    :param bd_lon:百度坐标经度
    :return:转换后的坐标列表形式
    """
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return [gg_lng, gg_lat]

def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret

def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret

def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]

def webmercator(lng,lat):#GPS-84转def webmercator
    x=lng*20037508.34/180
    y=math.log(math.tan((90+lat)*math.pi/360))/(math.pi/180)
    y=lat*20037508.34/180
    return[x,y]

if __name__ == '__main__':
    i=0
    f0= open('BD09.txt', 'w', encoding='utf-8')
    F0=open('GCJ-02.txt','w',encoding='utf-8')
    G=open('WGS-84.txt','w',encoding='utf-8')
    F=open('WebMercator.txt','w',encoding='utf-8')
    f=open('stations.txt','r',encoding='utf-8')
    lines=f.readlines()
    Lines=len(lines)
    for line in lines:
        lng=getlnglat(line)['result']['location']['lng']
        lat=getlnglat(line)['result']['location']['lat'] #得到百度api返回的经纬度坐标
        f0.write(str(lng)+'\t'+str(lat)+'\n') #保存到BD-09.txt
        lng0=bd09_to_gcj02(lng,lat)
        F0.write(str(lng0[0])+'\t'+str(lng0[1])+'\n')#保存到GCJ-02.txt
        Lng=gcj02_to_wgs84(lng0[0],lng0[1])
        G.write(str(Lng[0])+'\t'+str(Lng[1])+'\n')#保存到WGS-84.txt
        W=webmercator(Lng[0],Lng[1])
        F.write(str(W[0])+'\t'+str(W[1])+'\n')#保存到WebMercator.txt
        i=i+1
        print('已经完成%d/%d'%(i,Lines))

