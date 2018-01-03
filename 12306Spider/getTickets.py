# _*_ coding:utf-8 _*_

"""
    查询火车票余票工具

Usage:
    tickets.py [-h] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单

Example:
    python tickets.py 上海 南昌 2018-1-9
"""
from docopt import docopt
from stations import stations
import requests
from TrainTicket import TrainTicket

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def click():
    """command-line interface"""
    arguments = docopt(__doc__)

    # 始发站
    # 输入始发站中文，然后在stations里面查询该站代码
    from_station_china = arguments['<from>']
    if from_station_china in stations:
        from_station = stations.get(from_station_china)
    else:
        print("请输入有效的始发站")
        return 

    # 终点站
    # 输入终点站中文，然后在stations里面查询该站代码
    to_station_china = arguments['<to>']
    if to_station_china in stations:
        to_station = stations.get(to_station_china)
    else:
        print("请输入有效的终点站")
        return

    # 出发时间
    date = arguments['<date>']
    try:
        date = date.split('-')
        date = '%04d-%02d-%02d' % (int(date[0]), int(date[1]), int(date[2]))
    except:
        print("请输入有效的时间格式，例如：2018-1-9 或 2018-01-09")
        return

    # 构建URL，更换新的接口 
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'\
        .format(date, from_station, to_station)
    # 添加verify=False参数，说明不验证证书
    r = requests.get(url, verify=False)
    try:
        rows = r.json()['data']['result']
    except KeyError:
        print("请检查接口是否已更新")
        return 
    except:
        print("请检查日期是否正确")
        return 

    # 提取出信息中有用的部分
    new_rows = []
    for row in rows:
        split_row = row.split('|')
        new_rows.append(split_row[1:12] + split_row[13::])

    trains = TrainTicket(new_rows)
    info = ("{}-->{} ({}) 共计{}个车次").format(from_station_china, to_station_china, date, len(new_rows))
    print(info)
    trains.pretty_print()

if __name__ == '__main__':
    click()
