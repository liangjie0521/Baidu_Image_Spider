# -*- coding:UTF-8 -*-
import os


def setupDownloadDir(directory):
    """
    文件夹是否存在，不存在则新建文件夹
    """
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            pass
    return True


def isExists(filePath):
    return os.path.exists(filePath)
