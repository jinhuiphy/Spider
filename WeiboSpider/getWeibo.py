# -*- coding: UTF-8 -*-

from WeiboUser import WeiboUser
import traceback


def main():
    user_id = 1214435497    # 可以改成任意合法的用户id（爬虫的微博id除外）
    filte = 0      # 值为0表示爬取全部微博（原创微博+转发微博），值为1表示只爬取原创微博
    start_page = 1      # 1代表从第一条开始爬，会清空数据库，大于1代表续爬，不会清空之前的数据
    try:
        # 创建微博用户对象
        wb = WeiboUser(user_id, start_page, filte)
        # 爬取该微博用户信息
        wb.auto_get()

    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()


if __name__ == "__main__":
    main()
