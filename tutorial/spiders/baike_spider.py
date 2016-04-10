# -*- coding: utf-8 -*-
import scrapy
import re
import sys
from tutorial.items import DmozItem

class BaikeSpider(scrapy.Spider):
    name = "baike"
    allowed_domains = ["baike.baidu.com"]
    start_urls = [
        "http://www.baike.baidu.com/item/南瓜花",
    ]


    # def parse(self, response):
    #     for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
    #         print response.url, href.extract()
    #         url = response.urljoin(href.extract())
    #         yield scrapy.Request(url, callback=self.parse_dir_contents)
    #
    # def parse_dir_contents(self, response):
    #     for sel in response.xpath('//ul/li'):
    #         item = DmozItem()
    #         item['title'] = sel.xpath('a/text()').extract()
    #         item['link'] = sel.xpath('a/@href').extract()
    #         item['desc'] = sel.xpath('text()').extract()
    #         yield item


    def parse(self, response):
        suffix1 = "/descendant-or-self::*/text()"
        suffix2 = "/text()"
        suffix3 = "/descendant-or-self::*[not(self::span) and not(@class='image-link') and not(self::sup)]/text()"
        remove_white = lambda s: re.sub(r"\s+", "", s, flags=re.UNICODE)

        #introduce
        introduce = response.xpath("//div[@class='lemma-summary']/div[@class='para']"+suffix1).extract()
        print "".join(introduce).encode('utf-8')

        #basicInfo
        f_num = lambda n : "[" + str(n) + "]"
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
                print  "".join(key_data).replace(u"\xa0", "").strip().encode('utf-8')
                print  "".join(value_data).replace(u"\xa0", "").strip().encode('utf-8')
        basic_kv(basic_key_left, basic_value_left)
        basic_kv(basic_key_right, basic_value_right)
        print "\n"

        #detailPara
        f2 = lambda n : "//div[@class='para-title level-2'][" + str(n) + "]/h2[@class='title-text']"
        f3 = lambda n : "//div[@class='para-title level-2'][" + str(n) + "]/following::*/descendant-or-self::*" \
            "[(@class='para' or @class='title-text or self::a') and not(self::h2) and " \
            "count(preceding::div[@class='para-title level-2'])=" + str(n) + "]"
        f_title = lambda n : "(//div[@class='para-title level-2'][" + str(n) + "]/following::*/descendant-or-self::*" \
            "[self::h3 and count(preceding::div[@class='para-title level-2'])=" + str(n) + "])"
        f_data = lambda n, m : "(" + f_title(n,m) + "/parent::*/following::*/descendant-or-self::*" \
            "[(@class='para' or self::a) and not(self::h2) and not(self::h3)] intersect " + \
            f_title(n,m+1) + "/parent::*/preceding::*/descendant-or-self::*" + ")"
        key_num = int(float("".join(response.xpath("count(//div[@class='para-title level-2'])").extract())))
        for i in range(1, key_num+1):
            key_data = response.xpath(f2(i) + suffix2).extract()
            value_data = response.xpath(f3(i) + suffix3).extract()
            title_num = int(float("".join(response.xpath("count(" + f_title(i) + ")").extract())))
            print remove_white("".join(key_data)).encode('utf-8')
            print remove_white("".join(value_data)).encode('utf-8')
            print title_num
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
                print remove_white("".join(title_data)).encode('utf-8')
                print remove_white("".join(value_data)).encode('utf-8')
            print "\n"

