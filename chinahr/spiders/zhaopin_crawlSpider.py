__author__ = 'bitfeng'

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from chinahr.items import JobInfoItem, ComInfoItem


class ZhaopinCrawlSpider(CrawlSpider):
    name = 'zhaopin'
    allowed_domain = ['zhaopin.com']

    urls = []
    for url in open('/Users/bitfeng/spiders/chinahr/zhaopin_start.txt', 'r'):
        urls.append(url.strip())
    start_urls = urls[0:1]

#    cities = []
#    for line in open('/Users/bitfeng/spiders/chinahr/city3.txt'):
#        cities.append(urllib.quote(line.strip()))

    rules = [
        Rule(LxmlLinkExtractor(restrict_xpaths=('//div[@class="pagesDown"]')), follow=True),
        Rule(LxmlLinkExtractor(allow=('http://jobs.zhaopin.com/',)), callback='parse_info', follow=False),
    ]

#    def parse_start_url(self, response):
#        urls = response.xpath('//div[@id="search_bottom_content_demo"]/div[@class="clearfixed"]/h1/a/@href').extract()
#        for url in urls:
#            for city in self.cities[1:]:
#                scrapy.Request('http://sou.zhaopin.com'+self.format_url_city(url, city))

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
        job_item['job_desc_detail'] = response.xpath('//div[@class="tab-inner-cont"][1]/*/text()').extract()
        job_item['job_desc_loc'] = response.xpath('//div[@class="tab-inner-cont"][1]/h2/text()').extract()

        com_item['url'] = response.xpath('//div[@class="company-box"]/p[@class="company-name-t"]/a/@href').extract()
        com_item['com_name'] = response.xpath('//div[@class="company-box"]/p[@class="company-name-t"]/a/text()').extract()
        com_item['com_detail'] = response.xpath('//div[@class="company-box"]/p[@class="company-name-t"]/ul/*/text()').extract()
        com_item['com_intro'] = response.xpath('//div[@class="tab-inner-cont"][2]/*/text()').extract()

        return job_item, com_item

#    def format_url_city(self, url, city):
#        dom = url.split('?')[0]
#        para = url.split('?')[1].split('&')
#        for i in range(len(para)):
#            if 'jl=' in para[i]:
#                para[i] = 'jl='+city
#            else:
#                pass
#        return dom+'?'+'&'.join(para)+'&p=1'+'&isadv=0'