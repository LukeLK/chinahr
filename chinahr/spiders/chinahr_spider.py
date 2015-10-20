# -*- coding: utf-8 -*-

# 中华英才网的spider，爬取job和company信息

__author__ = 'bitfeng'

import os
import scrapy
from chinahr.items import JobInfoItem, ComInfoItem
from chinahr.formatText import FormatText
from scrapy.loader import ItemLoader

# 参见liepin_crawlSpider
class ChinahrSpider(scrapy.Spider):

    name = 'chinahr'
    allowed_domains = ['chinahr.com']
    urls = []
    BASE_DIR = os.path.abspath('.')
    file_path = os.path.join(BASE_DIR, 'chinahr/spiders/chinahr_start.txt')
    for url in open(file_path, 'r'):
        urls.append(url.strip())
    start_urls = urls[0:1]
    ext = FormatText()

    # Spider默认处理start_urls的函数，进行复写
    def parse(self, response):
        maxPageNumStr = ''.join(response.xpath('//a[@class="paging_jz"][last()]/span/text()').extract())
        onePage = ''.join(response.xpath('//a[@class="paging_jzd"]/span/text()').extract()).strip()
        if maxPageNumStr.isdigit():
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

        jobItem = JobInfoItem()
        jobItem['job_category'] = response.meta['category']
        jobItem['url'] = response.url
        jobItem['job_name'] = response.xpath('//h1[@class="company_name"]/text()').extract()
        jobItem['job_company'] = response.xpath('//span[@class="subC_name"]/a/text()').extract()
        jobItem['job_update'] = response.xpath('//span[@class="detail_C_Date fl"]/text()').re(u'\d{1,4}-\d{1,2}-\d{1,2}')
        jobItem['job_salary'] = response.xpath('//div[@class="detail_C_info"]/span/strong/text()').extract()
        # jobItem['job_detail'] = response.xpath('//div[@class="detail_C_info"]/span/text()').extract()
        jobItem['job_recruNums'] = response.xpath('//div[@class="detail_C_info"]/span/text()').re(u'(?<=招聘人数：).*')
        jobItem['job_miniEdu'] = response.xpath('//div[@class="detail_C_info"]/span/text()').extract()[1]
        jobItem['job_experience'] = response.xpath('//div[@class="detail_C_info"]/span/text()').extract()[2]
        jobItem['job_reqSex'] = self.ext.strip_list(
            response.xpath('//p[@class="sub_infoMa"]/span/text()').re(u'(?<=性别要求[:，：])[\s\S]*'))
        jobItem['job_reqAge'] = response.xpath('//p[@class="sub_infoMa"]/span/text()').re(u'(?<=年龄[:，：])[\s\S]*')
        jobItem['job_benefits'] = response.xpath('//ul[@class="welf_list clear toggleWelfL"]/li/text()').extract()
        jobItem['job_location'] = response.xpath('//div[@class="job_desc"]/p[1]/a/text()').extract()
        jobItem['job_nature'] = response.xpath('//div[@class="job_desc"]/p[2]/text()').re(u'(?<=工作性质：)[\s\S]*')
        # jobItem['job_desc_detail'] = response.xpath('//p[@class="sub_infoMa"]/span/text()').extract()
        jobItem['job_desc_resp'] = self.ext.extract_text(
            response.xpath('//p[@class="detial_jobSec"]').re(u'(?<=岗位职责[:，：])[\s\S]*'))
        jobItem['job_desc_req'] = self.ext.extract_text(
            response.xpath('//p[@class="detial_jobSec"]').re(u'(?<=任职条件[:，：])[\s\S]*'))
        jobItem['job_desc_detail'] = self.ext.extract_text(
            response.xpath('//p[@class="detial_jobSec"]').re(u'(?<=其他福利[:，：])[\s\S]*'))
        return jobItem

    def parse_cominfo(self, response):
        comItem = ComInfoItem()
        comItem['url'] = response.url
        comItem['com_name'] = response.xpath('//span[@class="compTitle"]/text()').extract()
        comItem['com_benefits'] = response.xpath('//li[@class="benefits"]/ul/li/text()').extract()
        comItem['com_intro'] = self.ext.extract_text(
            response.xpath('//div[@class="comp_content clearfix"]/div[@class="about"]/div[@class="content"]').extract())
        comItem['com_bene_other'] = self.ext.extract_text(
            response.xpath('//div[@class="comp_content clearfix"]/div[@class="benefit"]/div[@class="content"]/text()').extract())
        comItem['com_level'] = response.xpath('//div[@class="fl on"]/span/text()').extract()
        comItem['com_industry'] = response.xpath('//ul[@class="detail_R_cList"]/li').re(u'(?<=行业：</span>)[\s\S]*(?=</li>)')
        comItem['com_nature'] = response.xpath('//ul[@class="detail_R_cList"]/li').re(u'(?<=性质：</span>)[\s\S]*(?=</li>)')
        comItem['com_size'] = response.xpath('//ul[@class="detail_R_cList"]/li').re(u'(?<=规模：</span>)[\s\S]*(?=</li>)')
        comItem['com_link'] = response.xpath('//ul[@class="detail_R_cList"]/li/a/@href').extract()
        return comItem