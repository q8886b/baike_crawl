# -*- coding: utf-8 -*-
import scrapy
import re
import sys
import urllib
import MySQLdb
import random
import traceback
import signal
import os
import errno
import time

from functools import wraps
# from tutorial.items import BaikeItem

class BaikeSpider():
    name = "baike"
    allowed_domains = ["baike.baidu.com"]
    file = open("data/valid.url")
    # start_urls = [url.strip() for url in file.readlines()]
    # start_urls = ["http://127.0.0.1:8000/" + str(i) + ".html" for i in range(1, 22969)]
    valid_tags = ['中药', '中药材', '中成药', '草药', '中草药', '方剂', '药材', '药方']  #remove 药用植物
    idx = 1
    file.close()
    db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='graduate', charset='utf8')
    cur = db.cursor()
    sql = "INSERT INTO medicine_expand VALUES (%s,%s,%s)"
    duplicates = set()
    items = set()

    def db_write(self, item):
        if item['value'] == "":
            return
        key = " ".join([item['item'], item['attribute']])
        if key in self.duplicates:
            print "duplicate key:", key
            return
        else:
            self.duplicates.add(key)
        self.cur.execute(self.sql, [item['item'], item['attribute'], item['value']])
        self.db.commit()

    def __del__(self):
        self.db.close()

    def start_requests(self):
        for i in range(self.idx, 22969):
            path = "offline_html/" + str(i) + ".html"
            file = open(path, 'rb')
            body = file.read()
            file.close()
            response = scrapy.http.HtmlResponse(path, body=body)
            # set timeout for parse process
            def handler(signum, frame):
                print "timeout index:", str(i)
                raise Exception("end of time")
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(30)
            try:
                self.parse(response)
            except Exception, exc:
                pass
            signal.alarm(0)

    def parse_offline(self, response):
        polysemants = response.xpath("//li[@class='item']/a/text()").extract()
        poly_urls = response.xpath("//li[@class='item']/a/@href").extract()
        current = response.xpath("//li[@class='item']/span/text()").extract()
        for i in range(0, len(polysemants)):
            if polysemants[i].encode('utf-8') in self.valid_tags and current[0].encode('utf-8') not in self.valid_tags:
                href = u'http://baike.baidu.com' + poly_urls[i]
                print "Jump with:", polysemants[i].encode('utf-8'), href.encode('utf-8')
                yield scrapy.Request(href, self.parse)
                return
        with open("offline_html/" + str(self.idx) + ".html", 'wb') as outfile:
            outfile.write(response.body)
            self.idx += 1
        return

    def parse(self, response):
        print self.idx
        self.idx += 1
        item = dict()
        # item['item'] = urllib.unquote(response.request.meta['redirect_urls'][0].split('/')[-1])
        # print item['item']
        title = response.xpath("//dd[@class='lemmaWgt-lemmaTitle-title']/h1/text()").extract()
        if len(title) != 0:
            item['item'] = title[0].encode('utf-8')
            if item['item'] in self.items:
                print "duplicate item:", item['item']
                return
            else:
                self.items.add(item['item'])
        suffix1 = "/descendant-or-self::*/text()"
        suffix2 = "/text()"
        suffix3 = "/descendant-or-self::*[not(self::span) and not(@class='image-link') and not(self::sup)]/text()"
        remove_white = lambda s: re.sub(r"\s+", "", s, flags=re.UNICODE)
        f_num = lambda n: "[" + str(n) + "]"


        #introduce
        introduce = response.xpath("//div[@class='lemma-summary']/div[@class='para']"+suffix1).extract()
        # print "".join(introduce).encode('utf-8')
        item['attribute'] = '真简介'
        item['value'] = "".join(introduce).encode('utf-8')
        self.db_write(item)

        #detailPara
        f2 = lambda n : "//div[@class='para-title level-2'][" + str(n) + "]/h2[@class='title-text']"
        f3 = lambda n : "//div[@class='para-title level-2'][" + str(n) + "]/following::*/descendant-or-self::*" \
            "[(@class='para' or @class='title-text or self::a') and not(self::h2) and " \
            "count(preceding::div[@class='para-title level-2'])=" + str(n) + "]"
        f_title = lambda n : "(//div[@class='para-title level-2'][" + str(n) + "]/following::*/descendant-or-self::*" \
            "[self::h3 and count(preceding::div[@class='para-title level-2'])=" + str(n) + "])"
        key_num = int(float("".join(response.xpath("count(//div[@class='para-title level-2'])").extract())))
        for i in range(1, key_num+1):
            key_data = response.xpath(f2(i) + suffix2).extract()
            # print remove_white("".join(key_data)).encode('utf-8')
            title_num = int(float("".join(response.xpath("count(" + f_title(i) + ")").extract())))
            if title_num == 0:
                value_data = response.xpath(f3(i) + suffix3).extract()
                # print remove_white("".join(value_data)).encode('utf-8')
                item['attribute'] = remove_white("".join(key_data)).encode('utf-8')
                item['value'] = remove_white("".join(value_data)).encode('utf-8')
                self.db_write(item)
            else:
                for j in range(1, title_num+1):
                    intersect = lambda upper, lower : upper + "[count(.|" + lower + ") = count(" + lower + ")]"
                    title_data = response.xpath(f_title(i) + f_num(j) +  suffix2).extract()
                    upper = f_title(i) + f_num(j) + "/parent::*/following-sibling::*"
                    if j < title_num:
                        lower = f_title(i) + f_num(j+1) + "/parent::*/preceding-sibling::*"
                    elif j == title_num and i < key_num:
                        lower = "//div[@class='para-title level-2']" + f_num(i+1) + "/preceding-sibling::*"
                    else:
                        lower = None
                    if lower == None:
                        value_data = response.xpath(upper+"[@class='para']"+suffix3).extract()
                    else:
                        value_data = response.xpath(intersect(upper,lower)+suffix3).extract()
                    if (title_data == []):
                        break
                    # print remove_white("".join(title_data)).encode('utf-8')
                    # print remove_white("".join(value_data)).encode('utf-8')
                    item['attribute'] = remove_white("".join(key_data)).encode('utf-8')
                    item['value'] = "$key$" + remove_white("".join(title_data)).encode('utf-8') + "\n" \
                                    + "$value$" + remove_white("".join(value_data)).encode('utf-8') + "\n"
                self.db_write(item)

        # basicInfo
        basic_key_left = "//dl[@class='basicInfo-block basicInfo-left']/dt[@class='basicInfo-item name']"
        basic_key_right = "//dl[@class='basicInfo-block basicInfo-right']/dt[@class='basicInfo-item name']"
        basic_value_left = "//dl[@class='basicInfo-block basicInfo-left']/dd[@class='basicInfo-item value']"
        basic_value_right = "//dl[@class='basicInfo-block basicInfo-right']/dd[@class='basicInfo-item value']"

        def basic_kv(key, value):
            upper_bound = 100
            for i in range(1, upper_bound):
                key_data = response.xpath(key + f_num(i) + suffix1).extract()
                value_data = response.xpath(value + f_num(i) + suffix1).extract()
                if key_data == []:
                    break
                # print  "".join(key_data).replace(u"\xa0", "").strip().encode('utf-8')
                # print  "".join(value_data).replace(u"\xa0", "").strip().encode('utf-8')
                item['attribute'] = "".join(key_data).replace(u"\xa0", "").strip().encode('utf-8')
                item['value'] = "".join(value_data).replace(u"\xa0", "").strip().encode('utf-8')
                if " ".join([item['item'], item['attribute']]) not in self.duplicates:
                    self.db_write(item)

        basic_kv(basic_key_left, basic_value_left)
        basic_kv(basic_key_right, basic_value_right)

        #onlyPara
        if key_num == 0:
            onlyPara = "//div[@label-module='para']"
            onlyPara_data = response.xpath(onlyPara + suffix3).extract()
            # print remove_white("".join(onlyPara_data)).encode('utf-8')
            item['attribute'] = '资料'
            item['value'] = remove_white("".join(onlyPara_data)).encode('utf-8')
            self.db_write(item)   #don't know why this line take effect even comment it!
        return

deal = BaikeSpider()
deal.start_requests()