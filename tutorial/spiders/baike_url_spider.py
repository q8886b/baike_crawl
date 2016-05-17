# -*- coding: utf-8 -*-
import scrapy
import re
import sys
import urllib
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field
from scrapy.http.request import Request

class BaikeUrlSpider(scrapy.Spider):
    name = 'baike_url'
    allowed_domains = ['baike.baidu.com']
    all_urls = set()

    start_urls = []
    valid_tags = ['中药', '中药材', '中成药', '草药', '中草药', '方剂', '药材', '药方', '药用植物']
    for valid_tag in valid_tags:
        start_urls.append("http://baike.baidu.com/taglist?tag=" + valid_tag)
    temp_list = []
    for url in start_urls:
        for i in range(0, 76):
            sub = url + "&offset=" + str(i*10)
            temp_list.append(sub)
    start_urls = temp_list

    # start_urls = ['http://baike.baidu.com/view/565498.htm']

    # file = open("data/medicine.url")
    # start_urls = [url.strip() for url in file.readlines()]
    # file.close()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 0}
                }
                #'origin_url': url
            })

    def url_valid(self, url):
        white = ['http://baike.baidu.com/item', 'http://baike.baidu.com/view', 'http://baike.baidu.com/subview']
        for prefix in white:
            if url.find(prefix) != -1:
                return True
        return False

    def parse(self, response):
        url = response.meta['splash']['args']['url']
        # print 'start parsing:', url
        source = False
        if self.url_valid(url.encode('utf-8')):
            tags = response.xpath("//span[@class='taglist']/text()").extract()
            for tag in tags:
                if tag.strip().encode('utf-8') in self.valid_tags:
                    if url in self.all_urls:
                        continue
                    else:
                        source = True
                        print url
                        self.all_urls.add(url)
                        break
        else:
            source = True

        if source:
            for href in response.xpath("//a/@href").extract():
                if href.find('http') == -1:
                    href = u'http://baike.baidu.com' + href
                if self.url_valid(href.encode('utf-8')):
                    # print 'start_url to be parsing:', href
                    yield scrapy.Request(href, self.parse, meta={
                        'splash': {
                            'endpoint': 'render.html',
                            'args': {'wait': 0}
                        }
                    })







