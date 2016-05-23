# coding=utf-8
import MySQLdb
import sys
import os
from qa_support import attributes


def find_item(words, attrs):
    db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='graduate', charset='utf8')
    cur = db.cursor()
    sql1 = "select item from medicine_simple where item = %s"
    sql2 = "select item from items where synonym = %s"
    #1 find item directly
    for word in words:
         cur.execute(sql1, [word.encode('utf-8')])
         for row in cur:
            return row[0]
    #2 find item in synonym
    for word in words:
        cur.execute(sql2, [word.encode('utf-8')])
        for row in cur:
            return row[0]
    #3 find item from attribute
    sql = 'select distinct item from medicine_simple where attribute = %s and value like %s'
    attrs_sample = [u'简介', u'功用', u'制备', u'用法', u'别名', u'性味', u'来源', u'鉴定', u'生态环境', u'成分',
                    u'归经', u'培育', u'毒性', u'禁忌', u'文化']
    item_weight = dict()
    while os.getcwd().split('/')[-1] != 'graduate':
        os.chdir("../")
    for attr in attrs:
        idx = attrs_sample.index(attr)
        filename = "data/" + str(idx+1) + ".dic"
        tfdic = attributes.TFDictionary(filename)
        valid_words = []
        for word in words:
            if tfdic.exist(word):
                valid_words.append(word)
        for word in valid_words:
            cur.execute(sql, [attr, '%'+word.encode('utf-8')+'%'])
            for row in cur:
                if item_weight.has_key(row[0]):
                    item_weight[row[0]] += tfdic.cal([word])
                else:
                    item_weight[row[0]] = 0.0
    # for k, v in item_weight.iteritems():
    #     print k, v
    return max(item_weight, key=item_weight.get)

        # print find_item([u"今天", u"天气", u"过山龙", u"蛇咬子", u"麻黄"])
# print find_item([u"今天", u"天气", u"过山龙", u"蛇咬子"])



