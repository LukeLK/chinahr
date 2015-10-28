# -*- coding: utf-8 -*-

# 中华英才网的spider，爬取job和company信息

__author__ = 'bitfeng'

import os
import scrapy
from chinahr.items import JobInfoItem, ComInfoItem
from scrapy.loader import ItemLoader
from chinahr.processors import *
import logging

# 参见liepin_crawlSpider
class ChinahrSpider(scrapy.Spider):

    name = 'chinahr'
    allowed_domains = ['chinahr.com']
    urls = []
    BASE_DIR = os.path.abspath('.')
    file_path = os.path.join(BASE_DIR, 'chinahr/spiders/chinahr_start.txt')
    for url in open(file_path, 'r'):
        urls.append(url.strip())
    start_urls = urls

    # Spider默认处理start_urls的函数，进行复写
    def parse(self, response):
        maxPageNumStr = ''.join(response.xpath('//a[@class="paging_jz"][last()]/span/text()').extract())
        onePage = ''.join(response.xpath('//a[@class="paging_jzd"]/span/text()').extract()).strip()
        if maxPageNumStr.isdigit():
            logging.warning('LEGAL_STARTURL:'+response.url)
            url_sec = response.url.split('/')
            url_head = '/'.join(url_sec[0:-1])
            urls_tail = [str(i*20) for i in range(int(maxPageNumStr))]
            urls = [url_head+'/p'+tail for tail in urls_tail]
            for url in urls:
                yield scrapy.Request(url, callback=self.parse_urls)
        elif int(onePage) == 1:
            yield scrapy.Request(response.url, callback=self.parse_urls)
        else:
            pass

    def parse_urls(self, response):
        job_urls = response.xpath('//a[@class="js_detail"]/@href').extract()
        com_urls = response.xpath('//a[@class="js_com_name"]/@href').extract()
        category = ''.join(response.xpath('//div[@class="crumb_jobs"]/span[last()]/text()').extract()).strip()

        for url in job_urls:
            yield scrapy.Request(url, callback=self.parse_jobinfo, meta={'category': category})
        for url in com_urls:
            yield scrapy.Request(url, callback=self.parse_cominfo, meta={'category': category})

    def parse_jobinfo(self, response):

        loader = ItemLoader(item=JobInfoItem(), response=response)
        loader.add_value('job_category', value=response.meta['category'])
        loader.add_value('url', value=response.url)        
        loader.add_xpath('job_name', '//h1[@class="company_name"]/text()', TakeFirstL())        
        loader.add_xpath('job_company', '//span[@class="subC_name"]/a/text()', TakeFirstL())        
        loader.add_xpath('job_update', '//span[@class="detail_C_Date fl"]', re=u'\d{1,4}-\d{1,2}-\d{1,2}')        
        loader.add_xpath('job_salary', '//div[@class="detail_C_info"]/span/strong/text()', TakeFirstL())        
        loader.add_xpath('job_recruNums', '//div[@class="detail_C_info"]/span/text()', re=u'(?<=招聘人数：).*')        
        loader.add_xpath('job_miniEdu', '//div[@class="detail_C_info"]/span/text()', TakeNumL(1))        
        loader.add_xpath('job_experience', '//div[@class="detail_C_info"]/span/text()', TakeNumL(2))
        loader.add_xpath('job_reqSex', '//p[@class="sub_infoMa"]/span/text()', TakeFirstL(), re=u'(?<=性别要求[:，：])[\s\S]*')
        loader.add_xpath('job_reqAge', '//p[@class="sub_infoMa"]/span/text()', TakeFirstL(), re=u'(?<=年龄[:，：])[\s\S]*')        
        loader.add_xpath('job_benefits', '//ul[@class="welf_list clear toggleWelfL"]/li/text()', JoinL('|'))        
        loader.add_xpath('job_location', '//div[@class="job_desc"]/p/a/text()', TakeFirstL())
        loader.add_xpath('job_nature', '//div[@class="job_desc"]/p/text()', TakeFirstL(), re=u'(?<=工作性质：)[\s\S]*')
        loader.add_xpath('job_desc_resp', '//p[@class="detial_jobSec"]', RemoveTagsL(), TakeFirstL(), re=u'(?<=岗位职责[:，：])[\s\S]*')        
        loader.add_xpath('job_desc_req', '//p[@class="detial_jobSec"]', RemoveTagsL(), TakeFirstL(), re=u'(?<=任职条件[:，：])[\s\S]*')        
        loader.add_xpath('job_desc', '//p[@class="detial_jobSec"]', RemoveTagsL(), TakeFirstL(), re=u'(?<=其他福利[:，：])[\s\S]*')

        return loader.load_item()

    def parse_cominfo(self, response):
        loader = ItemLoader(item=ComInfoItem(), response=response)
        loader.add_value('url', value=response.url)
        loader.add_xpath('com_name', '//span[@class="compTitle"]/text()', TakeFirstL())
        loader.add_xpath('com_benefits', '//li[@class="benefits"]/ul/li/text()', JoinL('|'))
        loader.add_xpath('com_intro', '//div[@class="comp_content clearfix"]/div[@class="about"]/div[@class="content"]', ExtractTextL(), TakeFirstL())
        loader.add_xpath('com_bene_other', '//div[@class="comp_content clearfix"]/div[@class="benefit"]/div[@class="content"]/text()', ExtractTextL(), TakeFirstL())
        loader.add_xpath('com_level', '//div[@class="fl on"]/span/text()', TakeFirstL())
        loader.add_xpath('com_industry', '//ul[@class="detail_R_cList"]/li', TakeFirstL(), re=u'(?<=行业：</span>)[\s\S]*(?=</li>)')
        loader.add_xpath('com_nature', '//ul[@class="detail_R_cList"]/li', TakeFirstL(), re=u'(?<=性质：</span>)[\s\S]*(?=</li>)')
        loader.add_xpath('com_size', '//ul[@class="detail_R_cList"]/li', TakeFirstL(), re=u'(?<=规模：</span>)[\s\S]*(?=</li>)')
        loader.add_xpath('com_link', '//ul[@class="detail_R_cList"]/li/a/@href', TakeFirstL())

        return loader.load_item()