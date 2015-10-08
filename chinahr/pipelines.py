# -*- coding: utf-8 -*-

__author__ = 'bitfeng'
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import re
import sys
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

#格式转换
class FormatItemPipeline(object):

    def process_item(self, item, spider):
        for key in item.keys():
            if type(item[key]) == list:#将list转换为string，并去掉\n
                if len(item[key]) == 0:
                    item[key] = 'null'
                elif len(item[key]) == 1:
                    item[key] = '/'.join(''.join(item[key]).split())
                else:
                    item[key] = ''.join('|'.join(item[key]).split())
            elif type(item[key] == str):#去掉string的\n
                item[key] = '/'.join(item[key].split())
            else:
                pass
        return item


#json格式，写json文件
class JsonWriterPipeline(object):

    #初始化
    def __init__(self):
        self.file_jobNum = 1
        self.file_comNum = 1
        self.maxNum = 1000000 #每个文件的最大行数

    #打开spider，同时打开json文件
    def open_spider(self, spider):
        self.file_job = open(spider.name+'-jobItem'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.jl', 'wb')
        self.file_com = open(spider.name+'-comItem'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.jl', 'wb')

    #关闭spider，同时关闭json文件
    def close_spider(self, spider):
        self.file_job.close()
        self.file_com.close()

    #处理spider返回的item，写job和com的json文件
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        if item.name() == 'JobInfoItem':
            if self.file_jobNum % self.maxNum == 0:
                self.file_job.close()
                self.file_job = open(spider.name+'-jobItem'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.jl', 'wb')
            else:
                pass
            self.file_job.write(line)
            self.file_jobNum += 1
        elif item.name() == 'ComInfoItem':
            if self.file_comNum % self.maxNum == 0:
                self.file_com.close()
                self.file_com = open(spider.name+'-comItem'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.jl', 'wb')
            else:
                pass
            self.file_com.write(line)
            self.file_comNum += 1
        else:
            pass
        return item
