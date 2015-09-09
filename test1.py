__author__ = 'bitfeng'
import scrapy
import urllib
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

cities = []
for line in open('/Users/bitfeng/spiders/chinahr/city3.txt'):
#    print line.strip()
#    print urllib.quote(line.strip())
    cities.append(urllib.quote(line.strip()))

#print cityUrl[0]
url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=530&bj=7002000&sj=015'
city = 'city'
dom = url.split('?')[0]
para = url.split('?')[1].split('&')
print para
for i in range(len(para)):
    if 'jl=' in para[i]:
        para[i] = 'jl='+'%E5%B9%BF%E5%B7%9E'
    else:
        pass
print para
maxPageNum = random.randint(500, 1000)
scraped_url = dom+'?'+'&'.join(para)+'&p=1'+'&isadv=0'
print scraped_url

print '--------------'

nums = [u'\u4e0a\u4e00\u9875', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'...', u'\u4e0b\u4e00\u9875']
max_num = 0
print len(nums)
if len(nums) == 0:
    print 0
else:
    for i in range(len(nums)):
        if nums[i].isdigit():
            max_num = i
            print max_num
        else:
            pass
    print max_num

print '--------------'
job_item = {}
response = HtmlResponse(url='http://sou.zhaopin.com/jobs/searchresult.ashx?bj=4082000&sj=158&jl=%E5%B9%BF%E5%B7%9E&p=1&isadv=0')
#print 'response:'+response.url
print response
print Selector(response=response)
maxNum = Selector(response=response).xpath('//div[@class="pagesDown"]/ul/li/a/text()').extract()
print maxNum
job_item['url'] = response.url
job_item['job_name'] = Selector(response=response).xpath('//div[@class="inner-left fl"][1]/h1/text()')
job_item['job_desc_loc'] = Selector(response=response).xpath('//ul[@class="terminal-ul clearfix"]/li/strong/text()')

print job_item
urls = []
for line in open('/Users/bitfeng/spiders/chinahr/zhaopin_startURL.txt', 'r'):
    urls.append(line.strip())
urls_pro_locs = []
for url in urls:
    for city in cities:
        dom = url.split('?')[0]
        para = url.split('?')[1].split('&')
        for i in range(len(para)):
            if 'jl=' in para[i]:
                para[i] = 'jl='+city
            else:
                pass
        urls_pro_locs.append(dom+'?'+'&'.join(para)+'&p=1'+'&isadv=0')
print len(cities)
print len(urls_pro_locs)
#fw = open('/Users/bitfeng/spiders/chinahr/zhaopin_start.txt', 'wb')
#for url in urls_pro_locs:
#    fw.write(url+'\n')
#fw.close()

urls = []
for url in open('/Users/bitfeng/spiders/chinahr/zhaopin_start.txt', 'r'):
    urls.append(url.strip())
start_urls = urls[0]
print scraped_url
