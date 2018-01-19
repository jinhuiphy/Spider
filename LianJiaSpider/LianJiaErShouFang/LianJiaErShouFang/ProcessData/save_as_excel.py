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
    print("正在将数据写入excel，请稍后")
    for house in db.find({}):
        row += 1
        if row == 1:
            wa.append(["名称", "房屋价格", "房屋单价", "税费", "房间类型",
                       "楼层", "方位", "房屋类型", "面积", "年份",
                       "小区名称","所在区域", "经度", "纬度", "地铁",
                       "看房时间", "链家编号", "url"])
        else:
            address = city + house['areaName']
            lng, lat = getLocation(address)
            wa.append([house['name'], house['price'], house['unitPrice'], house['tax'], house['room'],
                       house['floor'], house['direction'], house['type'], house['area'], house['year'],
                       house['communityName'],house['areaName'], lng, lat, house['subway'],
                       house['visitTime'], house['houseRecord'], house['url']])
    wb.save(path)

def saveDataOnly(db, path):
    """只将数据库内的数据保存为xlsx格式，不涉及经纬"""
    wb = Workbook()
    wa = wb.active

    row = 0
    print("正在将数据写入excel，请稍后")
    for house in db.find({}):
        row += 1
        if row == 1:
            wa.append(["名称", "房屋价格", "房屋单价", "税费", "房间类型",
                       "楼层", "方位", "房屋类型", "面积", "年份", "小区名称",
                       "所在区域", "地铁", "看房时间", "链家编号", "url"])
        else:
            wa.append([house['name'], house['price'], house['unitPrice'], house['tax'], house['room'],
                       house['floor'], house['direction'], house['type'], house['area'], house['year'],
                       house['communityName'],house['areaName'], house['subway'],
                       house['visitTime'], house['houseRecord'], house['url']])
    wb.save(path)

def getLocation(city):
    """"通过调用百度的API，获得地理位置的经纬度"""
    print(city)
    city = city.strip()
    city = city.split("（")[0]
    city = city.split(" ")[0]

    print(city)
    ak = '你的百度API的ak值'
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
    city = 'ChangSha'
    city_china = '长沙'
    dbClient = pymongo.MongoClient(host='localhost', port=27017)
    LianJia = dbClient['LianJiaErShouFang']
    ErShouFang = LianJia[city + 'ErShouFang']
    if not ErShouFang.find({}).count():
        print("该数据库为空，请检查要保存的城市名是否正确")
        return

    startPath = 'Data/' + city + 'ErShouFang/'
    if not os.path.exists(startPath):
        os.makedirs(startPath)
    filePath = startPath + city + 'ErShouFang.xlsx'

    saveDataOnly(ErShouFang, filePath)
    # saveData(ErShouFang, filePath, city_china)


if __name__ == "__main__":
    main()
