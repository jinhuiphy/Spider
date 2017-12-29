import pymongo
import pandas as pd
import matplotlib.pyplot as plt
def main():
    Client = pymongo.MongoClient(host='localhost', port=27017)
    Douban = Client['Douban']
    commentData = Douban['commentdata']
    data = pd.DataFrame(list(commentData.find()))
    # data['rate'] = pd.to_datetime(data['rate'])
    dict = data['rate'].value_counts()
    print(dict)
    sum = 0
    for i in range(len(dict)):
        sum+=(i+1)*dict[i]
    ave = 2*sum/len(data)
    print("ave:%.2f" %ave)
    # print(data['rate'])


if __name__ == '__main__':
    main()

