# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#职位信息
class JobInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_category = scrapy.Field()#工作类别
    url = scrapy.Field()#内容页面的url
    job_name = scrapy.Field()#工作名称
    job_company = scrapy.Field()#招聘企业名称
    job_update = scrapy.Field()#更新时间
    job_salary = scrapy.Field()#薪酬
    job_location = scrapy.Field()#招聘城市城区
    job_experience = scrapy.Field()#工作经历
    job_recruNums = scrapy.Field()#招聘人数
    job_nature = scrapy.Field()#工作性质（全职、兼职等）
    job_miniEdu = scrapy.Field()#最低学历
    job_detail = scrapy.Field()#其他细节
    job_benefits = scrapy.Field()#工作福利

    job_desc_loc = scrapy.Field()#工作详细地址
    job_desc_type = scrapy.Field()#描述信息中的工作类型
    job_desc_detail = scrapy.Field()#描述中的细节
    job_desc_resp = scrapy.Field()#工作职责
    job_desc_req =scrapy.Field()#工作要求
    job_condition = scrapy.Field()#工作内容

    #Item类型
    def name(self):
        return 'JobInfoItem'

#企业信息
class ComInfoItem(scrapy.Item):
    url = scrapy.Field()#内容页url
    com_name = scrapy.Field()#企业名称
    com_benefits = scrapy.Field()#企业福利
    com_detail = scrapy.Field()#企业细节
    com_intro = scrapy.Field()#企业介绍
    com_level = scrapy.Field()#企业VIP级别-Ex：chinahr的VIP2
    com_bene_other = scrapy.Field()#其他福利
    com_nature = scrapy.Field()#企业性质-Ex：国有、私有等
    com_size = scrapy.Field()#企业规模-Ex：100-199人
    com_industry = scrapy.Field()#企业所属行业
    com_address = scrapy.Field()#企业地址
    com_zipCode = scrapy.Field()#企业地址邮编

    #Item类型
    def name(self):
        return 'ComInfoItem'
