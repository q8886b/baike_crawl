# -*- coding: utf-8 -*-
import scrapy
import re
import sys
import urllib
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field
from scrapy.http.request import Request

class TooSimpleSpider(scrapy.Spider):
    name = 'simple'
    allowed_domains = ['baike.baidu.com']

    start_urls = ['http://baike.baidu.com/view/']
    baike_max = 19000000
    valid_tags = ['中药', '中药材', '中成药', '草药', '中草药', '方剂', '药材', '药方', '药用植物']

    def start_requests(self):
        for i in range(1, self.baike_max):
            url = self.start_urls[0] + str(i) + ".htm"
            yield Request(url, self.parse)

    def parse(self, response):
        if response.url.find('error') == -1:
            tags = response.xpath("//span[@class='taglist']/text()").extract()
            item = response.xpath("//dd[@class='lemmaWgt-lemmaTitle-title']/h1/text()").extract()[0]
            for tag in tags:
                if tag.strip().encode('utf-8') in self.valid_tags:
                    print item.strip(), tag.strip(), response.url
                    break
        else:
            print "error", response.url






