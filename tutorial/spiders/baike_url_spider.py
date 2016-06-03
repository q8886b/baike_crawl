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

    valid_tags = ['中药', '中药材', '中成药', '草药', '中草药', '方剂', '药材', '药方', '药用植物']

    file = open("data/known.url")
    known_urls = set([url.strip() for url in file])
    file.close()

    file = open("data/baike.url")
    start_urls = [url.strip() for url in file]
    file.close()

    file = open("data/valid.url")
    valid_urls = set([url.strip() for url in file])
    file.close()

    attrs = set()
    file = open("data/attribute_synonym.txt")
    for line in file:
        for word in line.split():
            attrs.add(word.strip().decode('utf-8'))
    file.close()

    def start_requests(self):
        """
        with open("data/exchange.txt", 'rb') as infile, open("data/known.url", 'a') as outfile1, \
            open("data/valid.url", 'a') as outfile2:
            for line in infile:
                if line.find("known") == -1:
                    outfile2.write(line)
                else:
                    outfile1.write(line)
        """

        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 0, 'image':0},
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
        for href in response.xpath("//div[@class='zhixin-box']/descendant-or-self::*/a/@href").extract():
            if href.find('http') == -1:
                href = u'http://baike.baidu.com' + href
            if self.url_valid(href.encode('utf-8')):
                if href not in self.known_urls:
                    yield scrapy.Request(href, self.parse_valid)

    def parse_valid(self, response):
        print "new known:", response.url
        self.known_urls.add(response.url)
        url = response.url
        tags = response.xpath("//span[@class='taglist']/text()").extract()

        #1 see whether tag is right
        for tag in tags:
            if tag.strip().encode('utf-8') in self.valid_tags:
                print "n v:", url
                return
        """
        #2 see whether content is right
        remove_white = lambda s: re.sub(r"\s+", "", s, flags=re.UNICODE)
        def k_parse(total):
            rsuit = u"【[^】]*】[^【]*"
            sl = re.findall(rsuit, total, re.UNICODE)

            rkey = u"【[^】]*】"
            S = set()
            for s in sl:
                key = re.findall(rkey, s, re.UNICODE)[0].strip(u"【】")
                S.add(key)
            return S
        # check whether k is an standard attribute
        def k_in_keys(k, keys):
            for kk in keys:
                if k.find(kk) != -1:
                    return True
            return False
        keyword = "//h2[@class='title-text'] "
        content = "//div[@class='para']/text()"
        keys1 = response.xpath(keyword).extract()
        contents = response.xpath(content).extract()
        keys2 = k_parse(remove_white("".join(content)))
        keys = set(keys1) | keys2
        total = 1
        valid = 1
        for k in keys:
            if k_in_keys(k, self.attrs):
                valid += 1
                total += 1
            else:
                total += 1
        if float(valid)/total > 0.8:
            print "n v:", url
        return
        """






