# coding=utf-8
import csv
import re
import MySQLdb
import os
import sys
import urllib

if os.getcwd().split('/')[-1] == 'public':
    os.chdir("../../")

ATTR_NUM = 15
ITEM_NOT_FOUND = u"找不到您说的中草药哦～"
ATTR_NOT_FOUND = u"找不到答案哦～"
input = urllib.unquote(sys.argv[1]).decode('utf-8')
output = u""


attrs = [set() for x in xrange(ATTR_NUM)]
with open("data/key.txt", 'rb') as infile:
    for i in range(15):
        line = infile.readline().decode('utf-8')
        for word in line.split():
            attrs[i].add(word)
            # print i, word
items = set()
with open("data/valid_items.txt", 'rb') as infile:
    for line in infile:
        if line == "":
            continue
        items.add(line.strip().decode('utf-8'))
        # print line.strip().decode('utf-8')

def find_item(input):
    for item in items:
        if input.find(item) != -1:
            return item
    return None

def find_attr(input):
    idx_found = set()
    for idx in range(ATTR_NUM):
        for a in attrs[idx]:
            if input.find(a) != -1:
                idx_found.add(idx)
                break
    return idx_found


item = find_item(input)
idx_found = find_attr(input)
if item is None:
    output = ITEM_NOT_FOUND
else:
    db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='graduate', charset='utf8')
    cur = db.cursor()
    sql = "select attribute, value from medicine where item = %s and attribute like %s"
    answers = set()
    for idx in idx_found:
        for attr in attrs[idx]:
            cur.execute(sql, [item.encode('utf-8'), '%'+attr.encode('utf-8')+'%'])
            for result in cur.fetchall():
                answers.add(result[0] + u'@' + result[1])
    if answers == set():
        output = ATTR_NOT_FOUND
    else:
        for answer in answers:
            attr = answer.split('@')[0]
            value = answer.split('@')[1]
            output += item + u"的" + attr + u": " + value + u"\n"
print output.encode('utf-8')






