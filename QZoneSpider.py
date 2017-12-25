from selenium import webdriver
import time
import pymongo
import csv

def login(driver, targetQQ, account, password):
    """ login account """
    driver.get('http://user.qzone.qq.com/{}/311'.format(targetQQ))
    time.sleep(2)
    try:
        driver.find_element_by_id('login_div')
        login_div_exit = True
    except:
        login_div_exit = False
    if login_div_exit:
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('switcher_plogin').click()
        driver.find_element_by_id('u').clear()
        driver.find_element_by_id('u').send_keys(account)
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys(password)
        driver.find_element_by_id('login_button').click()
        time.sleep(3)
    # driver.implicitly_wait(3)

def getData(driver, db):
    content = driver.find_elements_by_css_selector('.content')
    mtime = driver.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
    # like = driver.find_element_by_css_selector('.qz_like_btn.c_tx.mr8')
    try:
        tail = driver.find_element_by_css_selector('.custom-tail').text
        tail_exit = True
    except:
        tail = "Null"
        tail_exit = False
    for con, mti in zip(content, mtime):
        data = {
            'time': mti.get_attribute("title"),
            'Mood': con.text,
            'tail': tail
        }

        db.insert_one(data)

def printData(db):
    for i in db.find():
        print(i)

def saveCookie(cookie):
    cookie_dict = []
    for c in cookie:
        ck = "{0}={1};".format(c['name'], c['value'])
        cookie_dict.append(ck)
    return cookie_dict

def printCookie(cookie_dict):
    i = ''
    for c in cookie_dict:
        i += c
    print('Cookies:', i)

def getOneQQ(driver, targetQQ, account, password, targetPage, db):
    print("QQ：" + targetQQ + "=========>开始")

    Mood = db[targetQQ]
    if Mood.find():
        Mood.remove({})

    login(driver, targetQQ, account, password)

    try:
        driver.find_element_by_id('QM_OwnerInfo_Icon')
        owner_info_exit = True
    except:
        owner_info_exit = False
        print('你没有权限访问')
    if owner_info_exit == True:
        driver.switch_to.frame('app_canvas_frame')
        driver.implicitly_wait(3)
        page=0
        try:
            while page<targetPage:
                page+=1
                print("QQ: " + targetQQ + " page: " + str(page) + "正在读取")
                getData(driver, Mood)
                driver.find_element_by_link_text(u"下一页").click()
                print("QQ: " + targetQQ + " page: " + str(page) + "读取完毕")
                time.sleep(1)
        except:
            print("QQ: " + targetQQ + " 超出页面数量")
        # printData(Mood)
        print("QQ: " + targetQQ + "=========>完成")

def mian():
    driver = webdriver.Chrome()
    # driver.maximize_window()

    # cookie = driver.get_cookies()

    conn = pymongo.MongoClient(host='localhost', port=27017)    # set database
    qzone = conn['qzone']

    targetQQ = '1234567'
    account = '1234567'
    password = '1234567'
    targetPage = 20

    # csv_reader = csv.reader(open(r'C:\Users\Jack\PycharmProjects\Spider\QQmail.csv'))
    # for qq in csv_reader:
    #     targetQQ=qq[2]
    #     print(targetQQ)
    #     getOneQQ(driver, targetQQ, account, password, targetPage, qzone)
    getOneQQ(driver, targetQQ, account, password, targetPage, qzone)
    driver.close()
    driver.quit()

if __name__ == '__main__':
    mian()
