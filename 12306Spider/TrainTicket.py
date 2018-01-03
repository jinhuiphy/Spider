# _*_ coding:utf-8 _*_
__author__ = "lvhaidong"
__modifier__ = "jinhuiphy"

from prettytable import PrettyTable
from stations import stations

# 将stations的字典key和value调转，方便根据代码得到中文地址
stations = dict(zip(stations.values(), stations.keys()))

# 拿到对应的火车票进行显示
class TrainTicket(object):
    """docstring for TrainTicket"""
    def __init__(self, rows):
        self.rows = rows
        self.header = '车次 出发/到达站 出发/到达时间 历时(H/M) 商务座 一等座 二等座 高级软卧 软卧 动卧 硬卧 软座 硬座 无座 其他'.split()

    # 查看运行的时间
    def __get_duration(self, row):
        if row[9] == "99:59":
            return "--"
        duration = row[9].replace(':','小时') + "分"

        # 如果是不足一小时的,应该是去掉前面的4位, 只剩下分钟数,例如00H:25M 武清->北京
        if duration.startswith('00'):
            return duration[4:]

        # 当大于1小时的,就从第一位取值,显示小时数
        elif duration.startswith('0'):
            return duration[1:]
        return duration

    # 根据列表返回的字段,进行获取,拿到对应的值
    @property
    def trains(self):
        for row in self.rows:
            from_station, to_station = "过", "过"
            if row[3] == row[5]:
                from_station = "始"
            if row[4] == row[6]:
                to_station = "终"

            arrive = "当日到达"
            if row[7].replace(':', '') > row[8].replace(':', ''):
                arrive = "次日到达"
            if row[9] == "99:59":
                arrive = "列车停运"

            train = [
                # 车次
                '\n'.join([row[2], row[1]]),
                # 出发 到达站
                '\n'.join([ "\033[0;31;1m" + from_station + "\033[0m" + stations.get(row[5]),
                            "\033[0;34;1m" + to_station + "\033[0m" + stations.get(row[6])]),
                # 出发 到达时间
                '\n'.join(["\033[0;31;1m"+row[7]+"\033[0m",
                            "\033[0;34;1m"+ row[8] + "\033[0m"]),
                # 历时
                '\n'.join([self.__get_duration(row),
                            arrive]),
                # 商务座
                row[-5] if row[-5] else '--',
                # 一等座
                row[-6] if row[-6] else '--',
                # 二等座
                row[-7] if row[-7] else '--',
                # 高等软卧
                row[-16] if row[-16] else '--',
                # 软卧
                row[-14] if row[-14] else '--',
                # 动卧
                row[-4] if row[-4] else '--',
                # 硬卧
                row[-9] if row[-9] else '--',
                # 软座
                row[-13] if row[-13] else '--',
                # 硬座
                row[-8] if row[-8] else '--',
                # 无座
                row[-11] if row[-11] else '--',
                # 其他
                row[-15] if row[-15] else '--',
            ]

            # 内置函数,循环遍历
            yield train

    # 格式化打印
    def pretty_print(self):
        """
            数据已经获取到了，剩下的就是提取我们要的信息并将它显示出来。
            prettytable这个库可以让我们它像MySQL数据库那样格式化显示数据。
        """
        pt = PrettyTable()

        # 设置每一列的标题
        pt._set_field_names(self.header)

        # 添加每一行
        for train in self.trains:
            pt.add_row(train)

        print(pt)

