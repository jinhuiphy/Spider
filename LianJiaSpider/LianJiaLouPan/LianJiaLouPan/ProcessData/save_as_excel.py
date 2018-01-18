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
    for loupan in db.find({}):
        row += 1
        if row == 1:
            wa.append(["楼盘名称", "物业类型", "楼盘价格", "楼盘位置", "经度", "纬度", "状态", "URL"])
        else:
            address = city + loupan['where']
            lng, lat = getLocation(address)
            wa.append([loupan['name'], loupan['wuye'], loupan['price'], loupan['where'], lng, lat, loupan['state'], loupan['url']])

    wb.save(path)

def getLocation(city):
    """"通过调用百度的API，获得地理位置的经纬度"""
    print(city)
    city = city.strip()
    city = city.split("（")[0]
    city = city.split(" ")[0]

    print(city)
    ak = '输入你自己的百度API ak值'
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
    city = 'ChongQing'
    city_china = '重庆'
    dbClient = pymongo.MongoClient(host='localhost', port=27017)
    LianJia = dbClient['LianJia']
    LouPan = LianJia[city + 'LouPan']

    startPath = 'Data/' + city + 'LouPan/'
    if not os.path.exists(startPath):
        os.makedirs(startPath)
    filePath = startPath + city + 'LouPan.xlsx'

    saveData(LouPan, filePath, city_china)


if __name__ == "__main__":
    main()
