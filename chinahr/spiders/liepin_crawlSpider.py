# -*- coding: utf-8 -*-

# 猎聘的spider，爬取job和company信息

__author__ = 'bitfeng'

import re
import scrapy
from chinahr.items import JobInfoItem, ComInfoItem
from scrapy.loader import ItemLoader
from chinahr.processors import *
import urllib

# 猎聘网spider
class LiepinCrawlSpider(scrapy.Spider):
    name = 'liepin'  # spider名称
    allowed_domain = ['liepin.com']  # 限制域名
    start_urls = ['http://www.liepin.com/it/?imscid=R000000030',   # 起始urls
                  'http://www.liepin.com/realestate/?imscid=R000000031',
                  'http://www.liepin.com/financial/?imscid=R000000032',
                  'http://www.liepin.com/consumergoods/?imscid=R000000033',
                  'http://www.liepin.com/automobile/?imscid=R000000034',
                  'http://www.liepin.com/medicine/?imscid=R000000054',
                  ]

    # 处理起始urls的response
    def parse(self, response):
        urls = response.xpath('//ul[@class="sidebar float-left"]/li/dl/dd/a/@href').extract()
        for url in urls:
            yield scrapy.Request('http://www.liepin.com'+re.sub(re.compile(u'&dqs=\d*'), '', url), callback=self.parse_flip)

    def parse_flip(self, response):
        category = ''.join(re.compile(u'(?<=&key=).*?(?=&)').findall(response.url))
        urls = response.xpath('//ul[@class="sojob-result-list"]/li/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_info, meta={'category': category})
        reg_url = ''.join(response.xpath('//div[@class="pagerbar"]').
                          re(u'(?<=<a class="current" href="javascript:;">)\d{1,3}</a>.*?(?=</a>)'))
        next_url = ''.join(re.compile(u'(?<=href=")http.*?(?=")').findall(reg_url))
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse_flip)

    # 抓取 职位信息 和 公司信息
    def parse_info(self, response):
        loaderJob = ItemLoader(item=JobInfoItem(), response=response)
        loaderJob.add_value('url', value=response.url)
        loaderJob.add_value('job_category', value=urllib.unquote(response.meta['category']))
        loaderJob.add_xpath('job_name', '//div[@class="title-info over"]/h1/text()')
        loaderJob.add_xpath('job_name', '//div[@class="title-info "]/h1/text()')
        loaderJob.add_xpath('job_company', '//div[@class="title-info over"]/h3/text()')
        loaderJob.add_xpath('job_company', '//div[@class="title-info "]/h3/text()')
        loaderJob.add_xpath('job_company', '//div[@class="title-info "]/h3/a/text()')
        loaderJob.add_xpath('job_miniEdu', '//div[@class="resume clearfix"]/span/text()', TakeNumL(0))
        loaderJob.add_xpath('job_experience', '//div[@class="resume clearfix"]/span/text()', TakeNumL(1))
        loaderJob.add_xpath('job_reqLan', '//div[@class="resume clearfix"]/span/text()', TakeNumL(2))
        loaderJob.add_xpath('job_reqAge', '//div[@class="resume clearfix"]/span/text()', TakeNumL(3))
        loaderJob.add_xpath('job_salary', '//p[@class="job-main-title"]/text()', TakeFirstL())
        loaderJob.add_xpath('job_location', '//p[@class="basic-infor"]/span[1]/text()', TakeFirstL())
        loaderJob.add_xpath('job_update', '//p[@class="basic-infor"]/span[2]/text()', TakeFirstL(), re=u'(?<=发布于：).*')
        loaderJob.add_xpath('job_desc', '//div[@class="content content-word"][1]', RemoveTagsL(), StripBlankL(), JoinL(''))
        loaderJob.add_xpath('job_benefits', '//div[@class="job-main main-message"]',
                            RemoveTagsL(), ReplaceBlank(), re=u'(?<=薪酬福利：)[\s\S]*')
        loaderJob.add_xpath('job_benefits', '//div[@class="tag-list clearfix"]/span/text()', JoinL('|'))
        yield loaderJob.load_item()

        if 'job.liepin.com' in response.url:
            loaderCom = ItemLoader(item=ComInfoItem(), response=response)
            loaderCom.add_value('url', value=response.url)
            loaderCom.add_value('com_name', value=loaderJob.get_collected_values('job_company'))
            loaderCom.add_xpath('com_industry', '//div[@class="right-post-top"]/div[@class="content content-word"]/a[1]/@title', TakeFirstL())
            loaderCom.add_xpath('com_size', '//div[@class="right-post-top"]/div[@class="content content-word"]', RemoveTagsL(), re=u'(?<=规模：)[\s\S]*?(?=<br>)')
            loaderCom.add_xpath('com_nature', '//div[@class="right-post-top"]/div[@class="content content-word"]', RemoveTagsL(), re=u'(?<=性质：)[\s\S]*?(?=<br>)')
            loaderCom.add_xpath('com_address', '//div[@class="right-post-top"]/div[@class="content content-word"]', RemoveTagsL(), re=u'(?<=地址：)[\s\S]*')
            loaderCom.add_xpath('com_intro', '//div[@class="job-main main-message noborder "]/div[@class="content content-word"]/text()', StripBlankL(), TakeFirstL())
            yield loaderCom.load_item()