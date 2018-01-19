from openpyxl import Workbook
import pymongo
import os
import json
from urllib.request import urlopen
from urllib.parse import quote
import string
import time


def saveData(db, path, city):
    """将数据保存为xlsx格式，方便后期处理"""

    wb = Workbook()
    wa = wb.active

    row = 0
    for zufang in db.find({}):
        row += 1
        if row%200 == 0:
            print("慢点吧，歇个几秒继续跑")
            time.sleep(2)
        if row == 1:
            wa.append(["名称", "价格", "面积", "户型", "楼层", "朝向", "地铁", "小区", "位置", "经度", "纬度", "时间", "URL"])
        else:
            address = city + zufang['location']
            lng, lat = getLocation(address)
            wa.append([zufang['name'], zufang['price'], zufang['area'], zufang['type'], zufang['floor'], zufang['direction'],
                       zufang['subway'], zufang['community'], zufang['location'], lng, lat, zufang['time'], zufang['url']])

    wb.save(path)

def getLocation(city):
    """"通过调用百度的API，获得地理位置的经纬度"""

    # 处理爬下来的地理位置
    print(city)
    city = city.strip()     # 去除首末位置的空格换行符
    city = city.split("（")[0]       # 去除括号里面的内容
    city = city.split(" ")[0]       # 去除空格后面的内容

    print(city)
    ak = '你的ak值'     # 你的百度API的ak值
    url = 'http://api.map.baidu.com/geocoder/v2/?address=' + city + '&output=json&ak=' + ak + '&callback=showLocation'
    # print(url)
    url = quote(url, safe = string.printable)
    try:
        page = urlopen(url).read().decode('utf-8')

        # 处理返回的json数据
        page = page.replace("showLocation&&showLocation(", "")
        page = page.replace(")", "")
        print(page)

        # 将数据转换为dict
        data_json = json.loads(page)
        data_dict = dict(data_json)
        lng = data_dict["result"]["location"]["lng"]
        lat = data_dict["result"]["location"]["lat"]
    except Exception as e:
        print("Error：", e)
        lng = 'null'
        lat = 'null'
    return lng, lat


def main():
    city = 'XiaMen'        # 用于匹配相应的数据库
    city_china = '厦门'       # 方便百度API调用
    dbClient = pymongo.MongoClient(host='localhost', port=27017)
    LianJia = dbClient['LianJiaZuFang']
    LouPan = LianJia[city + 'ZuFang']

    # 创建文件目录
    startPath = 'Data/' + city + 'ZuFang/'
    if not os.path.exists(startPath):
        os.makedirs(startPath)
    filePath = startPath + city + 'ZuFang.xlsx'

    # 将数据保存为xlsx格式
    saveData(LouPan, filePath, city_china)


if __name__ == "__main__":
    main()
