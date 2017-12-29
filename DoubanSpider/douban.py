import requests
import time
import random
from lxml import etree  # ingonered
import pymongo

def get_cookies(path):
    cookies = {}
    f_cookie = open(path, 'r')
    for line in f_cookie.read().split(';'):
        name, value = line.strip().split('=', 1)
        cookies[name] = value
    return cookies

def next_page(url, cookies, header):
    r = requests.get(url=url, cookies=cookies, headers=header).content
    soup = etree.HTML(r)
    return soup.xpath('//*[@id="paginator"]/a[3]/@href')

def html_prase(url, cookies, header):
    r = requests.get(url=url, cookies=cookies, headers=header).content
    return etree.HTML(r)

def getOnePage(db, html):
    for i in range(1, 21):
        # get comment
        comment = ''.join(html.xpath('//*[@id="comments"]/div[%s]/div[2]/p/text()' % i)).strip().replace('\n', ',')
        # get date
        date = html.xpath('//*[@id="comments"]/div[%s]/div[2]/h3/span[2]/span[3]/text()' % i)
        if date:
            date = ''.join(html.xpath('//*[@id="comments"]/div[%s]/div[2]/h3/span[2]/span[3]/text()' % i)).strip()
        else:
            date = ''.join(html.xpath('//*[@id="comments"]/div[%s]/div[2]/h3/span[2]/span[2]/text()' % i)).strip()
        # get rate
        rate = html.xpath('//*[@id="comments"]/div[%s]/div[2]/h3/span[2]/span[2]/@title' % i)
        for i in rate:
            if u'\u4e00' <= i <= u'\u9fff':
                rate = i.strip()
            else:
                rate = '还行'
        # save data
        data = {
            'date': date,
            'comment': comment,
            'rate': rate
        }
        db.insert_one(data)

def main():
    # initial url
    absolute = 'https://movie.douban.com/subject/26322642/comments'
    page1_url = 'https://movie.douban.com/subject/26322642/comments?start=0&limit=20&sort=new_score&status=P&percent_type='
    page2_url = 'https://movie.douban.com/subject/26322642/comments?start=20&limit=20&sort=new_score&status=P&percent_type='
    # initial header
    header = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
    # initial database
    Client = pymongo.MongoClient(host='localhost', port=27017)
    Douban = Client['Douban']
    commentData = Douban['commentdata']
    if commentData.find():
        commentData.remove({})
    # initial cookies
    cookies = get_cookies('cookie.txt')
    # initial arguments
    targetPage = 25
    currentPage = 1
    next_page_url = next_page(page2_url, cookies, header)
    # spider begin
    print("爬取开始--->>")
    while (currentPage <= targetPage and next_page_url != []):
        print('正在爬取第%s页' % currentPage)
        if currentPage == 1:
            html = html_prase(page1_url, cookies, header)
        else:
            html = html_prase(absolute + ''.join(next_page_url), cookies, header)
            next_page_url = next_page(absolute + ''.join(next_page_url), cookies, header)
        getOnePage(commentData, html)
        time.sleep(1 + float(random.randint(1, 100)) / 20)
        print('第%s页爬取完毕' % currentPage)
        currentPage += 1
    print("爬取结束--->>")

if __name__ == '__main__':
    main()
