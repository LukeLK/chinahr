# -*- coding: utf-8 -*-

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


class FormatItemPipeline(object):

    def process_item(self, item, spider):
        for key in item.keys():
            if type(item[key]) == list:
                if len(item[key]) == 0:
                    item[key] = 'null'
                elif len(item[key]) == 1:
                    item[key] = '/'.join(''.join(item[key]).split())
                else:
                    item[key] = ''.join('|'.join(item[key]).split())
            elif type(item[key] == str):
                item[key] = '/'.join(item[key].split())
        return item


class JsonWriterPipeline(object):

    def __init__(self):
        self.file_job = open('jobItem'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.jl', 'wb')
        self.file_com = open('comItem'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.jl', 'wb')
        self.file_jobNum = 1
        self.file_comNum = 1
        self.maxNum = 1000000

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.file_job.close()
        self.file_com.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        if 'job' in item['url']:
            if self.file_jobNum % self.maxNum == 0:
                self.file_job.close()
                self.file_job = open('jobItem'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.jl', 'wb')
            self.file_job.write(line)
            self.file_jobNum += 1
        elif 'company' in item['url']:
            if self.file_comNum % self.maxNum == 0:
                self.file_com.close()
                self.file_com = open('comItem'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.jl', 'wb')
            self.file_com.write(line)
            self.file_comNum += 1
        else:
            pass
        return item

    def strip_blankchr(self, str_sel):
        str_re = []
        for var in str_sel:
            if re.compile(u'^\s+$').match(var):
                str_re.append(var.strip())
        return str_re


class TxtWriterPipeline(object):

    def __init__(self):
        self.file_job = open('jobItem'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.txt', 'wb')
        self.file_com = open('comItem'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.txt', 'wb')
        self.file_jobNum = 1
        self.file_comNum = 1
        self.maxNum = 100000

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.file_job.close()
        self.file_com.close()

    def process_item(self, item, spider):
        line = ','.join(dict(item).values())+'\n'
        if '/job/' in item['url']:
            if self.file_jobNum % self.maxNum == 0:
                self.file_job.close()
                self.file_job = open('jobItem'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.txt', 'wb')
            self.file_job.write(line)
            self.file_jobNum += 1
        elif '/company/' in item['url']:
            if self.file_comNum % self.maxNum == 0:
                self.file_com.close()
                self.file_com = open('comItem'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.txt', 'wb')
            self.file_com.write(line)
            self.file_comNum += 1
        else:
            pass
        return item

