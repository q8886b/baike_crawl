# coding=utf-8
import csv
import re
import MySQLdb
import os
import sys
import urllib
from qa_support import divide
from qa_support import items
from qa_support import attributes

while os.getcwd().split('/')[-1] != 'graduate':
    os.chdir("../")

ATTR_NUM = 15
ITEM_NOT_FOUND = u"找不到中草药"
ATTR_NOT_FOUND = u"找不到答案"
if len(sys.argv) > 1:
    input = urllib.unquote(sys.argv[1]).decode('utf-8')
else:
    input = u"吃了保宫止血颗粒和金刚藤丸血还是不断怎么办"
output = u""


dicnames = ['data/attribute.dic', 'data/attribute_synonym.txt', 'data/valid_items.txt', 'data/item_synonym.txt',
            'data/value.dic']
dic = divide.Dictionary(dicnames)
words = dic.doubleMaxMatch(input)
print " ".join(words).encode('utf-8')
item = items.find_item(words)
print item.encode('utf-8')

attrs = attributes.find_attr(words)

if item is None:
    output = ITEM_NOT_FOUND
elif len(attrs) == 0:
    output = ATTR_NOT_FOUND
else:
    db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='graduate', charset='utf8')
    cur = db.cursor()
    sql = "select attribute, value from medicine_simple where item = %s and attribute = %s"
    answers = set()
    for attr in attrs:
        cur.execute(sql, [item.encode('utf-8'), attr.encode('utf-8')])
        for result in cur.fetchall():
            answers.add(result[0] + u'@' + result[1])
    if len(answers) == 0:
        output = ATTR_NOT_FOUND
    else:
        for answer in answers:
            attr = answer.split('@')[0]
            value = answer.split('@')[1]
            output += item + u"的" + attr + u": " + value + u"\n"
print output.encode('utf-8')






