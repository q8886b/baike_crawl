# coding=utf-8
import MySQLdb
import sys


def find_attr(words):
    db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='graduate', charset='utf8')
    cur = db.cursor()
    sql = 'select attribute from attributes where synonym = %s'
    attrs = set()
    for word in words:
        cur.execute(sql, [word.encode('utf-8')])
        for row in cur:
            print word.encode('utf-8'), row[0].encode('utf-8')
            attrs.add(row[0])
    for attr in attrs:
        print attr.encode('utf-8')
    return attrs

