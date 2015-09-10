__author__ = 'bitfeng'

import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from chinahr.items import JobInfoItem, ComInfoItem

class LiepinCrawlSpider(CrawlSpider):
    name = 'liepin'
    allowed_domain = ['liepin.com']
    start_urls = ['http://www.liepin.com/it/?imscid=R000000030',
                  'http://www.liepin.com/realestate/?imscid=R000000031',
                  'http://www.liepin.com/financial/?imscid=R000000032',
                  'http://www.liepin.com/consumergoods/?imscid=R000000033',
                  'http://www.liepin.com/automobile/?imscid=R000000034',
                  'http://www.liepin.com/medicine/?imscid=R000000054',
                  ]
    rules = [
        Rule(LxmlLinkExtractor(restrict_xpaths=('//div[@class="pagerbar"]')), follow=True),
        Rule(LxmlLinkExtractor(restrict_xpaths=('//ul[@class="sojob-result-list"]'), allow=('job.liepin.com', 'a.liepin.com')), callback='parse_info', follow=False),
    ]

    def parse_start_url(self, response):
        urls = response.xpath('//ul[@class="sidebar float-left"]/li/dl/dd/a/@href').extract()
        for url in urls:
            yield scrapy.Request('http://www.liepin.com'+re.sub(re.compile(u'&dqs=\d*'), '', url))

    def parse_info(self, response):
        job_item = JobInfoItem()
        com_item = ComInfoItem()
        job_item['url'] = response.url

        over = response.xpath('//div[@class="title-info over"]')
        if over:
            job_item['job_name'] = response.xpath('//div[@class="title-info over"]/h1/text()').extract()
            job_item['job_name'].insert(0, 'over:')
            job_item['job_company'] = response.xpath('//div[@class="title-info over"]/h3/text()').extract()
        else:
            job_item['job_name'] = response.xpath('//div[@class="title-info "]/h1/text()').extract()
            job_item['job_company'] = response.xpath('//div[@class="title-info "]/h3/text()').extract()
        job_item['job_detail'] = response.xpath('//div[@class="resume clearfix"]/span/text()').extract()
        job_item['job_salary'] = response.xpath('//p[@class="job-main-title"]/text()').extract()
        job_item['job_location'] = response.xpath('//p[@class="basic-infor"]/span[1]/text()').extract()
        job_item['job_update'] = response.xpath('//p[@class="basic-infor"]/span[2]/text()').extract()
        job_item['job_desc_resp'] = response.xpath('//div[@class="content content-word"][1]/text()').extract()

        if 'a.liepin.com/' in response.url:
            job_item['job_benefits'] = self.extract_text(response.xpath('//div[@class="content content-word"][3]/ul/li').extract())
            job_item['job_desc_detail'] = self.extract_text(response.xpath('//div[@class="content content-word"][2]/ul/li').extract())
            job_item['job_company'].insert(0, 'hunter:')
            return job_item
        else:
            job_item['job_benefits'] = response.xpath('//div[@class="tag-list clearfix"]/span/text()').extract()
            job_item['job_desc_detail'] = self.extract_text(response.xpath('//div[@class="content"]/ul/li').extract())
            com_item['url'] = response.xpath('//div[@class="right-post-top"]/a/@href').extract()
            com_item['com_industry'] = response.xpath('//div[@class="right-post-top"]/div[@class="content content-word"]/a[1]/@title').extract()
            com_detail = self.strip_blankchr(response.xpath('//div[@class="right-post-top"]/div[@class="content content-word"]/text()').extract())
            com_item['com_size'] = com_detail[0]
            com_item['com_nature'] = com_detail[1]
            com_item['com_address'] = com_detail[2]
            com_item['com_intro'] = response.xpath('//div[@class="job-main main-message noborder "]/div[@class="content content-word"]/text()').extract()
            return job_item, com_item

    def extract_text(self, str_sel):
        str_re = []
        pattern = re.compile(u'(?<=>)[\s\S]*?(?=<)')
        for var in str_sel:
            str_re.append(re.sub(u'\r?\n', '/', ''.join(pattern.findall(var))).replace(' ', ''))
        return str_re

    def strip_blankchr(self, str_sel):
        str_re = []
        for var in str_sel:
            if not re.compile(u'^\s+$').match(var):
                str_re.append(var.strip())
        return str_re