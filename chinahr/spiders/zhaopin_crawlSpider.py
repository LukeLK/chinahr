# -*- coding: utf-8 -*-

#智联招聘的spider，爬取job和company信息
__author__ = 'bitfeng'

import os
from scrapy.spiders import CrawlSpider, Rule  #使用CrawlSpider类
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from chinahr.items import JobInfoItem, ComInfoItem
from chinahr.formatText import FormatText


#参见liepin_crawlSpider
class ZhaopinCrawlSpider(CrawlSpider):
    name = 'zhaopin'
    allowed_domain = ['zhaopin.com']

    urls = []
    BASE_DIR = os.path.abspath('.')
    file_path = os.path.join(BASE_DIR, 'chinahr/spiders/zhaopin_start.txt')
    for url in open(file_path, 'r'):
        urls.append(url.strip())

    start_urls = urls
    ext = FormatText()

    rules = [
        Rule(LxmlLinkExtractor(restrict_xpaths=('//div[@class="pagesDown"]')), follow=True),
        Rule(LxmlLinkExtractor(allow=('http://jobs.zhaopin.com/',)), callback='parse_info', follow=False),
    ]

    def parse_info(self, response):
        job_item = JobInfoItem()
        com_item =ComInfoItem()
        job_item['url'] = response.url
        job_item['job_name'] = response.xpath('//div[@class="inner-left fl"][1]/h1/text()').extract()
        job_item['job_company'] = response.xpath('//div[@class="inner-left fl"][1]/h2/a/text()').extract()
        job_item['job_benefits'] = response.xpath('//div[@class="inner-left fl"][1]/div/span/text()').extract()
        job_item['job_salary'] = response.xpath('//ul[@class="terminal-ul clearfix"]/li[1]/strong/text()').extract()
        job_item['job_location'] = response.xpath('//ul[@class="terminal-ul clearfix"]/li[2]/strong/a/text()').extract()
        job_item['job_update'] = response.xpath('//ul[@class="terminal-ul clearfix"]/li[3]/strong/span/text()').extract()
        job_item['job_nature'] = response.xpath('//ul[@class="terminal-ul clearfix"]/li[4]/strong/text()').extract()
        job_item['job_experience'] = response.xpath('//ul[@class="terminal-ul clearfix"]/li[5]/strong/text()').extract()
        job_item['job_miniEdu'] = response.xpath('//ul[@class="terminal-ul clearfix"]/li[6]/strong/text()').extract()
        job_item['job_recruNums'] = response.xpath('//ul[@class="terminal-ul clearfix"]/li[7]/strong/text()').extract()
        job_item['job_category'] = response.xpath('//ul[@class="terminal-ul clearfix"]/li[8]/strong/a/text()').extract()
        job_item['job_desc_detail'] = self.ext.extract_text(response.xpath('//div[@class="tab-inner-cont"][1]').extract())
        job_item['job_desc_loc'] = response.xpath('//div[@class="tab-inner-cont"][1]/h2/text()').extract()
        com_item['url'] = response.xpath('//div[@class="company-box"]/p[@class="company-name-t"]/a/@href').extract()
        com_item['com_name'] = response.xpath('//div[@class="company-box"]/p[@class="company-name-t"]/a/text()').extract()
        com_item['com_detail'] = self.ext.extract_text(response.xpath('//div[@class="company-box"]/ul/li').extract())
        com_item['com_intro'] = self.ext.extract_text(response.xpath('//div[@class="tab-inner-cont"][2]').extract())

        return job_item, com_item

