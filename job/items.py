# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class JobItem(scrapy.Item):
    # define the fields for your item here like:
    source = scrapy.Field()
    source_url = scrapy.Field()
    job_title = scrapy.Field()
    company_title = scrapy.Field()
    updated_date = scrapy.Field()
    work_location = scrapy.Field()
    category = scrapy.Field()
    salary = scrapy.Field()
    level = scrapy.Field()
    deadline = scrapy.Field()
    experience = scrapy.Field()
    job_description = scrapy.Field()
    job_requirement = scrapy.Field()
    other_information = scrapy.Field()
    tags = scrapy.Field()

    
