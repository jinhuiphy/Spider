from openpyxl import Workbook
import pymongo
import os
import json
from urllib.request import urlopen
from urllib.parse import quote
import string


def saveData(db, path, city):
    """将数据保存为xlsx格式，方便后期处理"""
    wb = Workbook()
    wa = wb.active

    row = 0
    for zufang in db.find({}):
        row += 1
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
    print(city)
    city = city.strip()
    city = city.split("（")[0]
    city = city.split(" ")[0]

    print(city)
    ak = '这里填你的百度API的ak值'
    url = 'http://api.map.baidu.com/geocoder/v2/?address=' + city + '&output=json&ak=' + ak + '&callback=showLocation'
    # print(url)
    url = quote(url, safe = string.printable)
    # print(url)
    page = urlopen(url).read().decode('utf-8')
    # data_json = page.read().decode('utf-8')
    # data_json = json.loads(page)
    page = page.replace("showLocation&&showLocation(", "")
    page = page.replace(")", "")
    print(page)
    data_json = json.loads(page)
    data_dict = dict(data_json)
    if data_dict["status"] == 0:
        lng = data_dict["result"]["location"]["lng"]
        lat = data_dict["result"]["location"]["lat"]
    else:
        lng = 'null'
        lat = 'null'
    return lng, lat


def main():
    city = 'ChangSha'
    city_china = '长沙'
    dbClient = pymongo.MongoClient(host='localhost', port=27017)
    LianJia = dbClient['LianJiaZuFang']
    LouPan = LianJia[city + 'ZuFang']

    startPath = 'Data/' + city + 'ZuFang/'
    if not os.path.exists(startPath):
        os.makedirs(startPath)
    filePath = startPath + city + 'ZuFang.xlsx'

    saveData(LouPan, filePath, city_china)


if __name__ == "__main__":
    main()
