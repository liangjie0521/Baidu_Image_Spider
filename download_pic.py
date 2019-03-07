# -*- coding:UTF-8 -*-
from multiprocessing import Process, Queue, Pool
import os
import json
import requests
import time
import sys
import file_util

"""
下载抓取的图片
"""


class DownloadPic(object):
    def __init__(self, target):
        self.searchKey = target

    def getInfo(self):
        """
        获取存储在文本中的数据信息
        """
        res = []
        with open('data/info/%s.txt' % self.searchKey, 'r') as f:
            for line in f:
                data = json.loads(line)
                res.extend(data['data'])
        return res

    def get_images_info(self, info):
        """
        解析json数据
        """
        data = []
        for item in info:
            if len(item) > 0:
                url = item['objURL']
                if not 'http' in url:
                    url = item['middleURL']
                name = url[(url.rfind('/')+1):]
                directory = os.path.join('data', 'images', self.searchKey)
                file_path = os.path.join(directory, name)
                data.append((
                    url, directory, file_path
                ))
                if 'replaceUrl' in item:
                    replace_url = item['replaceUrl']
                    for replace_item in replace_url:
                        if 'ObjURL' in replace_item:
                            item_url = replace_item['ObjURL']
                        elif 'objURL' in replace_item:
                            item_url = replace_item['objURL']
                        if 'http' in item_url:
                            item_name = item_url[(item_url.rfind('/')+1):]
                            item_file_path = os.path.join(directory, item_name)
                            data.append((
                                item_url, directory, item_file_path
                            ))
        return data

    def download_one_pic(self, img):
        """
        下载一张图片
        """
        url, directory, file_path = img
        if not file_util.isExists(file_path):
            file_util.setupDownloadDir(directory)
            try:
                header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                          'Accept-Encoding': 'gzip, deflate',
                          'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                          'Cache-Control': 'max-age=0',
                          'Connection': 'keep-alive',
                          'Cache-Control': 'max-age=0',
                          'If-Modified-Since': 'Thu, 01 Jan 1970 00:00:00 GMT',
                          'If-None-Match': '6271bfcc25fcf9857cf36b80e569f0bb',
                          'Upgrade-Insecure-Requests': '1',
                          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
                response = requests.get(url, header)
                if response.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                else:
                    print('download %s error,%s' % (url, response.status_code))
            except Exception as e:
                print('error url is %s' % url)
                print(e)

    def download_pics(self, images, process=5):
        """
        多进程下载图片
        """
        startTime = time.time()
        pool = Pool(process)
        for img in images:
            pool.apply_async(self.download_one_pic(img))
        pool.close()
        pool.join()
        endTime = time.time()
        print('下载完毕，用时：%s秒' % (endTime-startTime))

    def start_download(self):
        info = self.getInfo()
        imgs = self.get_images_info(info)
        self.download_pics(imgs, process=5)
