# coding=utf-8
import MySQLdb
import sys

def find_item(words):
    db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='graduate', charset='utf8')
    cur = db.cursor()
    sql1 = "select item from medicine_simple where item = %s"
    sql2 = "select item from items where synonym = %s"
    for word in words:
         cur.execute(sql1, [word.encode('utf-8')])
         for row in cur:
            return row[0]
    for word in words:
        cur.execute(sql2, [word.encode('utf-8')])
        for row in cur:
            return row[0]

# print find_item([u"今天", u"天气", u"过山龙", u"蛇咬子", u"麻黄"])
# print find_item([u"今天", u"天气", u"过山龙", u"蛇咬子"])



