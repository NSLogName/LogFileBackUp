# -*- coding: utf-8 -*-
# @Time    : 2018/1/4 10:03
# @Author  : 'XCTY'
# @Site    : 
# @File    : LogFileBackUp.py

import logging
import os
import sys
import time
import shutil
import datetime

from logging.config import fileConfig
from math import floor

# logmnr文件夹路径
LOGMNR_PATH = "D:\\Desktop\\logmnr\\"

# logmntoper文件夹路径
LOGMNTOPER_PATH = "D:\\Desktop\\logmntoper\\"

# logmnr文件夹备份路径
LOGMNR_BACKUP_PATH = "D:\\Desktop\\backup\\logmnr\\"

# logmntoper文件夹备份路径
LOGMNTOPER_BACKUP_PATH = "D:\\Desktop\\backup\\logmntoper\\"

# 30个#号
SEAT_JH = "#" * 30

# 30个*号
SEAT_XH = "*" * 30


# Logger类
class Logger(object):
    logging.config.fileConfig(sys.path[0] + "\\logging.ini")
    defaultLogger = logging.getLogger('default')
    errorLogger = logging.getLogger('error')


# 时间类
class Time():
    # 获取当前时间
    @staticmethod
    def getNowTime():
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    # 计算时间差
    @staticmethod
    def timedelta(startTimeStr, endTimeStr):
        startTime = datetime.datetime.strptime(startTimeStr, '%Y-%m-%d %H:%M:%S')
        endTime = datetime.datetime.strptime(endTimeStr, '%Y-%m-%d %H:%M:%S')
        secInt = (endTime - startTime).seconds
        minStr = str(floor((secInt) / 60))
        secStr = str(secInt % 60)
        if int(minStr) <= 0:
            return '共计耗时' + secStr + '秒'
        else:
            return '共计耗时' + minStr + '分' + secStr + '秒'


# 格式化天日期 如：20180104 --> 2018\\01\\04
def formatDayStr(dayStr):
    dayStrList = list(dayStr)
    dayStrList.insert(4, "\\")
    dayStrList.insert(7, "\\")
    return ''.join(dayStrList)


# 获取指定后缀名文件列表
def searchFileForSuffix(dirPath, suffix):
    fileList = []
    for root, dirs, files in os.walk(dirPath):
        for file in files:
            if os.path.splitext(file)[1] == suffix:
                fileList.append(file)
    return fileList


# 根据日期进行文件分类
def classifyFileOfDay(dirPath, suffix):
    fileMap = {}
    for file in searchFileForSuffix(dirPath, suffix):
        fileDay = formatDayStr(os.path.splitext(file)[0].split("_")[0])
        tmp = fileMap.get(fileDay)
        if tmp:
            tmp.append(file)
        else:
            tmpList = [file]
            fileMap[fileDay] = tmpList
    return fileMap


# 创建多层目录
def mkDirs(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        return False


# 根据日期获取几天前的日期
def date2Key(date, day):
    tempDate = date - datetime.timedelta(days=day)
    return tempDate.strftime('%Y') + '\\' + tempDate.strftime('%m') + '\\' + tempDate.strftime('%d')


# 过滤今天和昨天的日志文件
def cutTodayAndYesterday(fileMap):
    date = datetime.date.today()
    todayKey = date2Key(date, 0)
    yesterdayKey = date2Key(date, 1)
    if fileMap.get(todayKey):
        fileMap.pop(todayKey)
    if fileMap.get(yesterdayKey):
        fileMap.pop(yesterdayKey)
    return fileMap


# 执行方法
def func(oldPath, newPath, suffix):
    myTime = Time()
    try:
        Logger.defaultLogger.info(SEAT_JH + "备份开始" + SEAT_JH)
        startTime = myTime.getNowTime()

        fileMap = cutTodayAndYesterday(classifyFileOfDay(oldPath, suffix))
        for key in fileMap:
            newDirPath = newPath + key
            mkDirs(newDirPath)
            fileList = fileMap.get(key)
            for file in fileList:
                shutil.move(oldPath + file, newDirPath)
            shutil.make_archive(newDirPath, "zip", root_dir=newDirPath)
            if os.path.isdir(newDirPath):
                shutil.rmtree(newDirPath)
            Logger.defaultLogger.info(key + "备份成功！")

        endTime = myTime.getNowTime()
        Logger.defaultLogger.info(SEAT_JH + "备份结束" + SEAT_JH)
    except:
        Logger.errorLogger.info("备份出错！！！！")

    Logger.defaultLogger.info(SEAT_XH + "本次版本库备份" + myTime.timedelta(startTime, endTime) + SEAT_XH + "\n\n")


# 主方法
def mainFunc():
    Logger.defaultLogger.info("备份logmntoper文件夹内文件！")
    if os.path.exists(LOGMNTOPER_PATH):
        func(LOGMNTOPER_PATH, LOGMNTOPER_BACKUP_PATH, ".log")
    else:
        Logger.defaultLogger.info("logmntoper文件夹路径不存在！")

    Logger.defaultLogger.info("备份logmnr文件夹内文件！")
    if os.path.exists(LOGMNR_PATH):
        func(LOGMNR_PATH, LOGMNTOPER_BACKUP_PATH, ".log")
    else:
        Logger.defaultLogger.info("logmnr文件夹路径不存在！")


if __name__ == "__main__":
    mainFunc()
