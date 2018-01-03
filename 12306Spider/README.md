# 12306——Spider

用来爬取指定始发站和终点站以及日期所有车次的余票

参考项目：

https://github.com/protream/iquery

https://github.com/lvhaidong/TrainTicket

---
使用方法
---

 1. 安装所需的库

    `pip install prettytable docopt requests`

 2. 获取车站代码对应表

    `python getStations.py > stations.py`

    然后在字典前面加上`stations = `

    ![](https://github.com/jinhuiphy/Spider/blob/master/12306Spider/pictures/stations.png)

 3. 运行getTickets.py即可

    格式如下： 
    `python getTickets.py <from_station> <to_sation> <year-month-day>`

    ![](https://github.com/jinhuiphy/Spider/blob/master/12306Spider/pictures/tickets.png)







