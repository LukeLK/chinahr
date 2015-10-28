# -*- coding: utf-8 -*-

__author__ = 'bitfeng'
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import sys
import datetime
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import logging
from scrapy import log


reload(sys)
sys.setdefaultencoding('utf-8')


# 格式转换
class FormatItemPipeline(object):
    def process_item(self, item, spider):
        for key in item.keys():
            if type(item[key]) == list:  # 将list转换为string
                if '' in item[key]:
                    item[key].remove('')
                else:
                    pass
                if len(item[key]) == 0:
                    item[key] = 'null'
                elif len(item[key]) == 1:
                    item[key] = item[key][0]
                else:
                    item[key] = '|'.join(item[key])
        return item


# json格式，写json文件
class JsonWriterPipeline(object):

    # 初始化
    def __init__(self):
        self.file_jobNum = 1
        self.file_comNum = 1
        self.maxNum = 1000000  # 每个文件的最大行数

    # 打开spider，同时打开json文件
    def open_spider(self, spider):
        self.file_job = open(spider.name+'-jobItem'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.jl', 'wb')
        self.file_com = open(spider.name+'-comItem'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.jl', 'wb')

    # 关闭spider，同时关闭json文件
    def close_spider(self, spider):
        self.file_job.close()
        self.file_com.close()

    # 处理spider返回的item，写job和com的json文件
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        if item.classname() == 'JobInfoItem':
            if self.file_jobNum % self.maxNum == 0:
                self.file_job.close()
                self.file_job = open(spider.name+'-jobItem'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.jl', 'wb')
            else:
                pass
            self.file_job.write(line)
            self.file_jobNum += 1
        elif item.classname() == 'ComInfoItem':
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


# MYSQL数据库，dbpool线程池，实现异步插入数据
class MySQLPipeline(object):

    def __init__(self, MYSQL_URI):
        self.mysql_uri = MYSQL_URI

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            MYSQL_URI=crawler.settings.get('MYSQL_URI'),
        )

    def open_spider(self, spider):
        self.dbpool = adbapi.ConnectionPool(
            'MySQLdb',
            host=self.mysql_uri['host'],
            port=self.mysql_uri['port'],
            db=self.mysql_uri['db'],
            user=self.mysql_uri['user'],
            passwd=self.mysql_uri['passwd'],
            cursorclass=MySQLdb.cursors.DictCursor,
            charset=self.mysql_uri['charset'],
            use_unicode=True)

    def close_spider(self, spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        # run db query in thread pool
        if item.classname() == 'JobInfoItem':
            query = self.dbpool.runInteraction(self._job_insert, item)
        elif item.classname() == 'ComInfoItem':
            query = self.dbpool.runInteraction(self._com_insert, item)
        query.addErrback(self.handle_error)

        return item

    def _job_insert(self, tx, item):
        # create record if doesn't exist.
        # all this block run on it's own thread
        tx.execute("select * from job where url = %s", (item['url'],))
        result = tx.fetchone()
        if result:
            logging.log(logging.DEBUG, "Item already stored in db: %s" % item['url'])
        else:
            itemdict = dict(item)
            sqli = "insert into job(insert_time," \
                   "job_category," \
                   "url," \
                   "job_name," \
                   "job_company," \
                   "job_update," \
                   "job_salary," \
                   "job_location," \
                   "job_experience," \
                   "job_recruNums," \
                   "job_nature," \
                   "job_miniEdu," \
                   "job_detail," \
                   "job_benefits," \
                   "job_desc_loc," \
                   "job_desc," \
                   "job_desc_resp," \
                   "job_desc_req," \
                   "job_reqSex," \
                   "job_reqAge," \
                   "job_reqLan) " \
                   "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

            tx.execute(sqli, (datetime.datetime.now(),
                              itemdict.setdefault('job_category', None),
                              itemdict.setdefault('url', None),
                              itemdict.setdefault('job_name', None),
                              itemdict.setdefault('job_company', None),
                              itemdict.setdefault('job_update', None),
                              itemdict.setdefault('job_salary', None),
                              itemdict.setdefault('job_location', None),
                              itemdict.setdefault('job_experience', None),
                              itemdict.setdefault('job_recruNums', None),
                              itemdict.setdefault('job_nature', None),
                              itemdict.setdefault('job_miniEdu', None),
                              itemdict.setdefault('job_detail', None),
                              itemdict.setdefault('job_benefits', None),
                              itemdict.setdefault('job_desc_loc', None),
                              itemdict.setdefault('job_desc', None),
                              itemdict.setdefault('job_desc_resp', None),
                              itemdict.setdefault('job_desc_req', None),
                              itemdict.setdefault('job_reqSex', None),
                              itemdict.setdefault('job_reqAge', None),
                              itemdict.setdefault('Job_reqLan', None),)
                       )
            logging.log(logging.DEBUG, "Item stored in db: %s" % item['url'])
    
    def _com_insert(self, tx, item):
        # create record if doesn't exist.
        # all this block run on it's own thread
        tx.execute("select * from company where url = %s", (item['url'],))
        result = tx.fetchone()
        if result:
            logging.log(logging.DEBUG, "Item already stored in db: %s" % item['url'])
        else:
            itemdict = dict(item)
            sqli = "insert into company(insert_time," \
                   "url," \
                   "com_name," \
                   "com_benefits," \
                   "com_detail," \
                   "com_intro," \
                   "com_level," \
                   "com_bene_other," \
                   "com_nature," \
                   "com_size," \
                   "com_industry," \
                   "com_address," \
                   "com_link," \
                   "com_zipCode) " \
                   "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            
            tx.execute(sqli, (datetime.datetime.now(),
                              itemdict.setdefault('url', None),
                              itemdict.setdefault('com_name', None),
                              itemdict.setdefault('com_benefits', None),
                              itemdict.setdefault('com_detail', None),
                              itemdict.setdefault('com_intro', None),
                              itemdict.setdefault('com_level', None),
                              itemdict.setdefault('com_bene_other', None),
                              itemdict.setdefault('com_nature', None),
                              itemdict.setdefault('com_size', None),
                              itemdict.setdefault('com_industry', None),
                              itemdict.setdefault('com_address', None),
                              itemdict.setdefault('com_link', None),
                              itemdict.setdefault('com_zipCode', None),)
                       )
            logging.log(logging.DEBUG, "Item stored in db: %s" % item['url'])

    def handle_error(self, e):
        log.err(e)