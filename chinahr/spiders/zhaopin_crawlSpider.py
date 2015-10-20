# -*- coding: utf-8 -*-

# 智联招聘的spider，爬取job和company信息
__author__ = 'bitfeng'

import os
from scrapy.spiders import CrawlSpider, Rule  # 使用CrawlSpider类
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from chinahr.items import JobInfoItem, ComInfoItem


# 参见liepin_crawlSpider
class ZhaopinCrawlSpider(CrawlSpider):
    name = 'zhaopin'
    allowed_domain = ['zhaopin.com']

    urls = []
    BASE_DIR = os.path.abspath('.')
    file_path = os.path.join(BASE_DIR, 'chinahr/spiders/zhaopin_start.txt')
    for url in open(file_path, 'r'):
        urls.append(url.strip())

    start_urls = urls

    rules = [
        Rule(LxmlLinkExtractor(restrict_xpaths=('//div[@class="pagesDown"]')), follow=True),
        Rule(LxmlLinkExtractor(allow=('http://jobs.zhaopin.com/',)), callback='parse_info', follow=False),
    ]

    def parse_info(self, response):
        job_item = JobInfoItem()
        com_item = ComInfoItem()

        job_item['url'] = response.url
        job_item['job_name'] = response.xpath('//div[@class="inner-left fl"][1]/h1/text()').extract()
        job_item['job_company'] = response.xpath('//div[@class="inner-left fl"][1]/h2/a/text()').extract()
        job_item['job_benefits'] = response.xpath('//div[@class="inner-left fl"][1]/div/span/text()').extract()
        divs = response.xpath('//ul[@class="terminal-ul clearfix"]/li')
        job_item['job_salary'] = divs.re(u'(?<=职位月薪：</span><strong>).*(?=</strong></li>)')
        job_item['job_location'] = divs.re(u'(?<=工作地点：</span><strong>).*(?=</strong></li>)')
        job_item['job_update'] = divs.re(u'(?<=发布日期：</span><strong>).*(?=</strong></li>)')
        job_item['job_nature'] = divs.re(u'(?<=工作性质：</span><strong>).*(?=</strong></li>)')
        job_item['job_experience'] = divs.re(u'(?<=工作经验：</span><strong>).*(?=</strong></li>)')
        job_item['job_miniEdu'] = divs.re(u'(?<=最低学历：</span><strong>).*(?=</strong></li>)')
        job_item['job_recruNums'] = divs.re(u'(?<=招聘人数：</span><strong>).*(?=</strong></li>)')
        job_item['job_category'] = divs.re(u'(?<=职位类别：</span><strong>).*(?=</strong></li>)')
        job_item['job_desc_detail'] = response.xpath('//div[@class="tab-inner-cont"][1]').extract()
        job_item['job_desc_resp'] = response.xpath('//div[@class="tab-inner-cont"][1]').re(u'(?<=岗位职责|工作职责).*?(?=任职资格)')
        job_item['job_desc_req'] = response.xpath('//div[@class="tab-inner-cont"][1]').re(u'(?<=任职资格).*?(?=。)')
        job_item['job_desc_loc'] = response.xpath('//div[@class="tab-inner-cont"][1]/h2/text()').extract()

        com_item['url'] = response.xpath('//div[@class="company-box"]/p[@class="company-name-t"]/a/@href').extract()
        com_item['com_name'] = response.xpath('//div[@class="company-box"]/p[@class="company-name-t"]/a/text()').extract()
        divs = response.xpath('//div[@class="company-box"]/ul/li')
        com_item['com_size'] = divs.re(u'(?<=公司规模[:,：]).*')
        com_item['com_nature'] = divs.re(u'(?<=公司性质[:,：]).*')
        com_item['com_industry'] = divs.re(u'(?<=公司行业[:,：]).*')
        com_item['com_intro'] = response.xpath('//div[@class="tab-inner-cont"][2]').extract()
        com_item['com_link'] = divs.re(u'(?<=公司主页[:,：]).*')
        com_item['com_address'] = divs.re(u'(?<=公司地址[:,：])[\s\S]*(?=</strong>)')

        return job_item, com_item

