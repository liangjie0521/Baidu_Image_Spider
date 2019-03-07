# -*- coding:UTF-8 -*-
import requests
import json
from download_pic import DownloadPic
import file_util
import sys


class load_info(object):
    def __init__(self, word):
        self.__searchKey = word
        self.__header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                         'Accept-Encoding': 'gzip, deflate',
                         'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                         'Cache-Control': 'max-age=0',
                         'Connection': 'keep-alive',
                         'Cache-Control':'max-age=0',
                         'If-Modified-Since': 'Thu, 01 Jan 1970 00:00:00 GMT',
                         'If-None-Match': '6271bfcc25fcf9857cf36b80e569f0bb',
                         'Upgrade-Insecure-Requests': '1',
                         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}

    def save_page_data(self, page_data):
        """
        保存信息
        """
        data = json.dumps(page_data)
        file_util.setupDownloadDir('data/info')
        with open('data/info/%s.txt' % self.__searchKey, 'a') as f:
            f.write(data)
            f.write('\n')

    def load_page_info(self):
        """
        调用请求获取图片数据
        """
        page = 1
        next = True
        while True == next:
            url = 'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%s&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&word=%s&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&fr=&expermode=&force=&pn=%d&rn=30&gsm=1c2&1551775746980=' % (
                self.__searchKey, self.__searchKey, 551760)
            print(url)
            page_data = requests.get(url, self.__header).json()
            next = len(page_data['data']) > 1
            if next:
                self.save_page_data(page_data)
                page += 1

    def do_spider(self):
        self.load_page_info()
        download_pic = DownloadPic(self.__searchKey)
        download_pic.start_download()


if __name__ == "__main__":
    search_key = str(input('请输入搜索关键字'))
    load = load_info(search_key)
    load.do_spider()
