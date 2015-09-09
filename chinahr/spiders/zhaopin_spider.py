__author__ = 'bitfeng'

import urllib
import scrapy
from chinahr.items import JobInfoItem, ComInfoItem

class ZhaopinSpider(scrapy.Spider):
    name = 'zhaopin_a'
    allowed_domains = ['zhaopin.com']
    start_urls = ['http://sou.zhaopin.com']

    cityUrl = []
    for line in open('/Users/bitfeng/spiders/chinahr/city3.txt'):
        cityUrl.append(urllib.quote(line.strip()))

    def fomat_url_city(self, url, city):
        dom = url.split('?')[0]
        para = url.split('?')[1].split('&')
        print para
        for i in range(len(para)):
            if 'jl=' in para[i]:
                para[i] = 'jl='+city
            else:
                pass
        print para
#        maxPageNum = random.randint(500, 1000)
        return dom+'?'+'&'.join(para)+'&p=1'+'&isadv=0'

    def parse(self, response):

        divs = response.xpath('//div[@id="search_bottom_content_demo"]/div[@class="clearfixed"]').extract()
        for div in divs:
            urls_pro_loc = []
            cata = ''.join(div.xapth('./p/a/text()').extract()).strip()
            cla = ''.join(div.xapth('./h1/a/text()').extract()).strip()
            urls = div.xpath('./h1/a/@href').extract()
            for url in urls:
                for city in self.cityUrl:
                    self.fomat_url_city(url, city)
                    urls_pro_loc.append('http://sou.zhaopin.com'+format(url, city))
            for url in urls_pro_loc:
                yield scrapy.Request(url, callback=self.parse_Page)

    def parse_page(self, response):
        nums = response.xpath('//div[@class="pagesDown"]/ul/li/a/text()').extract()
        max_page_num = self.max_num(nums)
        catalog = ''.join(response.xpath('//div[@class="industry industry-small"]/input/@value').extract()).strip()
        urls = response.xpath('//div[@class="pagesDown"]/ul/li/a/@href').extract()
        job_urls = response.xpath('//td[@class="zwmc"]/div/a/@href').extract()
        for url in job_urls:
            yield scrapy.Request(url, callback=self.parse_jobinfo, meta={'catalog': catalog})
        if max_page_num != 0:
            for url in urls:
                yield scrapy.Request(url, callable=self.parse_page, meta={'catalog': catalog})
        else:
            pass

    def next_page(nums):
        if len(nums)==0:
            return 0
        else:
            max_page_num = 0
            for i in range(len(nums)):
                if nums[i].isdigit():
                    max_page_num = i
                else:
                    pass
            return max_page_num





