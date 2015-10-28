# -*- coding: utf-8 -*-

# 智联招聘的spider，爬取job和company信息
__author__ = 'bitfeng'

import os
import scrapy
from chinahr.items import JobInfoItem, ComInfoItem
from scrapy.loader import ItemLoader
from chinahr.processors import *
import logging


# 参见liepin_crawlSpider
class ZhaopinCrawlSpider(scrapy.Spider):
    name = 'zhaopin'
    allowed_domain = ['zhaopin.com']

    urls = []
    BASE_DIR = os.path.abspath('.')
    file_path = os.path.join(BASE_DIR, 'chinahr/spiders/zhaopin_start.txt')
    for url in open(file_path, 'r'):
        urls.append(url.strip())

    start_urls = urls

    def parse(self, response):
        urls = response.xpath('//div[@class="newlist_list_content"]').re(u'(?<=href=")http://jobs.zhaopin.com/.*?(?=")')
        if urls:
            logging.warning('LEGAL_STARTURL:'+response.url)
            for url in urls:
                yield scrapy.Request(url, callback=self.parse_info)
            reg_url = ''.join(response.xpath('//div[@class="pagesDown"]').
                              re(u'(?<=<a href="#" class="current">)\d{1,3}</a>.*?(?=</a>)'))
            next_url = ''.join(re.compile(u'(?<=href=")http.*?(?=")').findall(reg_url))
            if next_url:
                yield scrapy.Request(next_url, callback=self.parse)

    def parse_info(self, response):

        loaderJob = ItemLoader(item=JobInfoItem(), response=response)
        loaderCom = ItemLoader(item=ComInfoItem(), response=response)
        loaderJob.add_value('url', value=response.url)
        loaderJob.add_xpath('job_name', '//div[@class="inner-left fl"][1]/h1/text()', TakeFirstL())
        loaderJob.add_xpath('job_company', '//div[@class="inner-left fl"][1]/h2/a/text()', TakeFirstL())
        loaderJob.add_xpath('job_benefits', '//div[@class="inner-left fl"][1]/div/span/text()', JoinL('|'))
        divs = '//ul[@class="terminal-ul clearfix"]/li'
        loaderJob.add_xpath('job_salary', divs, TakeFirstL(), re=u'(?<=职位月薪：</span><strong>).*(?=</strong></li>)')
        loaderJob.add_xpath('job_location', divs, RemoveTagsL(), TakeFirstL(), re=u'(?<=工作地点：</span><strong>).*(?=</strong></li>)')
        loaderJob.add_xpath('job_update', divs, RemoveTagsL(), TakeFirstL(), re=u'(?<=发布日期：</span><strong>).*(?=</strong></li>)')
        loaderJob.add_xpath('job_nature', divs, TakeFirstL(), re=u'(?<=工作性质：</span><strong>).*(?=</strong></li>)')
        loaderJob.add_xpath('job_experience', divs, TakeFirstL(), re=u'(?<=工作经验：</span><strong>).*(?=</strong></li>)')
        loaderJob.add_xpath('job_miniEdu', divs, TakeFirstL(), re=u'(?<=最低学历：</span><strong>).*(?=</strong></li>)')
        loaderJob.add_xpath('job_recruNums', divs, TakeFirstL(), re=u'(?<=招聘人数：</span><strong>).*(?=</strong></li>)')
        loaderJob.add_xpath('job_category', divs, RemoveTagsL(), TakeFirstL(), re=u'(?<=职位类别：</span><strong>).*(?=</strong></li>)')
        loaderJob.add_xpath('job_desc', '//div[@class="tab-inner-cont"][1]', ExtractTextL(), StripBlankL(), JoinL('|'))
        loaderJob.add_xpath('job_desc_resp', '//div[@class="tab-inner-cont"][1]', ExtractTextL(), TakeFirstL(), re=u'(?<=岗位职责|工作职责).*?(?=任职资格|岗位要求)')
        loaderJob.add_xpath('job_desc_req', '//div[@class="tab-inner-cont"][1]', ExtractTextL(), TakeFirstL(), re=u'(?<=任职资格|岗位要求).*?(?=。)')
        loaderJob.add_xpath('job_desc_loc', '//div[@class="tab-inner-cont"][1]/h2/text()', TakeFirstL())

        loaderCom.add_xpath('url', '//div[@class="company-box"]/p[@class="company-name-t"]/a/@href', TakeFirstL())
        loaderCom.add_xpath('com_name', '//div[@class="company-box"]/p[@class="company-name-t"]/a/text()', TakeFirstL())
        divs = '//div[@class="company-box"]/ul/li'
        loaderCom.add_xpath('com_size', divs, ExtractTextL(), TakeFirstL(),  re=u'(?<=公司规模[:,：]).*')
        loaderCom.add_xpath('com_nature', divs, ExtractTextL(), TakeFirstL(),  re=u'(?<=公司性质[:,：]).*')
        loaderCom.add_xpath('com_industry', divs, ExtractTextL(), TakeFirstL(),  re=u'(?<=公司行业[:,：]).*')
        loaderCom.add_xpath('com_intro', '//div[@class="tab-inner-cont"][2]', ExtractTextL(), StripBlankL(), JoinL('|'))
        loaderCom.add_xpath('com_link', divs, ExtractTextL(), TakeFirstL(),  re=u'(?<=公司主页[:,：]).*')
        loaderCom.add_xpath('com_address', divs, RemoveTagsL(), TakeFirstL(),  re=u'(?<=公司地址[:,：])[\s\S]*(?=</strong>)')

        return loaderJob.load_item(), loaderCom.load_item()

