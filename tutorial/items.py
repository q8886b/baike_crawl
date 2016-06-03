# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BaikeItem(scrapy.Item):
     item = scrapy.Field()
     attribute = scrapy.Field()
     value = scrapy.Field()