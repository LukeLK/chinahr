# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_category = scrapy.Field()
    url = scrapy.Field()
    job_name = scrapy.Field()
    job_company = scrapy.Field()
    job_update = scrapy.Field()
    job_salary = scrapy.Field()
    job_location = scrapy.Field()
    job_experience = scrapy.Field()
    job_recruNums = scrapy.Field()
    job_nature = scrapy.Field()
    job_miniEdu = scrapy.Field()
    job_detail = scrapy.Field()
    job_benefits = scrapy.Field()

    job_desc_loc = scrapy.Field()
    job_desc_type = scrapy.Field()
    job_desc_detail = scrapy.Field()
    job_desc_resp = scrapy.Field()
    job_desc_req =scrapy.Field()
    job_condition = scrapy.Field()

    job_remark = scrapy.Field()

    def name(self):
        return 'JobInfoItem'


class ComInfoItem(scrapy.Item):
    url = scrapy.Field()
    com_name = scrapy.Field()
    com_benefits = scrapy.Field()
    com_detail = scrapy.Field()
    com_intro = scrapy.Field()
    com_level = scrapy.Field()
    com_bene_other = scrapy.Field()
    com_nature = scrapy.Field()
    com_size = scrapy.Field()
    com_industry = scrapy.Field()
    com_address = scrapy.Field()
    com_zipCode = scrapy.Field()

    def name(self):
        return 'ComInfoItem'
