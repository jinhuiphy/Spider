# _*_ coding:utf-8 _*_

import re
import requests
from pprint import pprint
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 根据用户输入的出站, 到站 以及时间,里面 from_station 和 to_station 并不是汉字或者拼音，而是一个代号，而我们想要输入的是汉字或者拼音
# 这个url就是汉字转化为拼音以及代号的js库,库中包含了车站的中文名，拼音，简写和代号等信息,我们只想要车站的汉字和代号
url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8971"

# 添加verify=False参数不验证证书
response = requests.get(url, verify=False)

# 将服务器返回的代码转化为文字
text = response.text

# 获得站点的中文
stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', text)

# 转化为字典
stations = dict(stations)

# 将字典中的key,value进行倒转
# stations = dict(zip(stations.values(), stations.keys()))
pprint(stations, indent = 4)
# 将输出的结果重定向到stations.py文件中