# -*- coding: utf-8 -*-
import csv
import httplib
import requests
import re
import MySQLdb

# original csv to clean csv
"""
with open('../1.csv', 'rb') as csvfile, open('../2.csv', 'wb') as writefile:
    spamreader = csv.reader(csvfile, delimiter=',')
    s = set([])
    for row in spamreader:
        str = ",".join(row).replace("?", "").replace("。","")
        if str.find("？") == None:
            continue
        s.add(str)

    spamwriter = csv.writer(writefile)
    for str in s:
        # print si
        spamwriter.writerow(str.split(','))
"""

# from clean csv file to url
"""
with open('data/medicine.csv', 'rb') as infile, open('data/medicine.url', 'wb') as outfile:
    url_prefix = "http://www.baike.baidu.com/item/"
    spamreader = csv.reader(infile, delimiter=',')
    for row in spamreader:
        outfile.write(url_prefix + row[0] + "\n")
"""

# from clean csv file to item dictionary
"""
with open('data/medicine.csv', 'rb') as infile, open('data/item.dic', 'wb') as outfile:
    spamreader = csv.reader(infile, delimiter=',')
    for row in spamreader:
        outfile.write(row[0] + "\n")
"""

# count valid url from baike.com

"""
with open('data/item.dic', 'rb') as infile:
	url_prefix = "http://www.baike.com/wiki/"
	count = 0
	total = 0
	for item in infile:
		url = url_prefix + item
		url = url.decode('utf-8').encode('utf-8')
		request = requests.head(url)
		if request.status_code == 200:
			count+=1
			print item
		total+=1
		if total % 100 == 0:
			print "total: " + str(total)
			print "count: " + str(count)
"""

# list duplicate words
"""
with open('data/key.txt', 'rb') as infile:
    ss = set()
    ll = []
    for line in infile:
        sl = line.split()
        for s in sl:
            if s not in ss:
                ss.add(s)
            else:
                ll.append(s)
    for s in ll:
        print s
"""


# database get attribute from value
"""
def kv_parse(total):
    rsuit = u"【[^】]*】[^【]*"
    sl = re.findall(rsuit, total, re.UNICODE)

    rkey = u"【[^】]*】"
    M = {}
    for s in sl:
        key = re.findall(rkey, s, re.UNICODE)[0].strip(u"【】")
        value = re.split(rkey, s, re.UNICODE)[1]
        M[key] = value
    return M
# check whether k is an standard attribute
def k_in_keys(k, keys):
    for kk in keys:
        if k.find(kk) != -1:
            return True
    return False


with open("data/kv_in_value.txt", 'rb') as infile, open("data/kv_in_value_output.csv", 'wb') as outfile, \
        open("data/key.txt", 'rb') as keyfile:
    # 1 keys
    keys = set()
    for line in keyfile:
        line = line.decode('utf-8')
        sl = line.strip().split()
        for s in sl:
            keys.add(s)
    # 2 csv file
    csvwriter = csv.writer(outfile)
    # 3 mysql
    db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='graduate', charset='utf8')
    cur = db.cursor()
    cur.execute('select * from medicine')
    row = cur.fetchone()

    for line in infile:
        line = line.decode('utf-8')
        sl = line.split(u'\t')
        if len(sl) == 3:
            m = kv_parse(sl[2])
            for k, v in m.iteritems():
                if k_in_keys(k, keys):
                    sql = "delete from medicine where item = %s and attribute = %s;"
                    cur.execute(sql, [sl[0].encode('utf-8'), sl[1].encode('utf-8')])
                    db.commit()
                    writeline = [sl[0].encode('utf-8'), k.encode('utf-8'), v.encode('utf-8')]
                    csvwriter.writerow(writeline)
                else:
                    print sl[1], k
    cur.close()
    db.close()

with open("data/kv_in_value_output.csv", 'rb') as infile:
    db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='graduate', charset='utf8')
    cur = db.cursor()
    spamreader = csv.reader(infile, delimiter=',',quotechar='"')
    sql = "insert into medicine values (%s, %s, %s)"
    D = ["一", "二", "三", "四", "五", "六"]
    keys = []
    for line in spamreader:
        key = line[0]+line[1]
        keys.append(key)
        if keys.count(key) == 1:
            cur.execute(sql, [line[0].strip(), '>'+line[1].strip(), line[2].strip()])
        else:
            cur.execute(sql, [line[0].strip(), '>'+line[1].strip()+str(keys.count(key)), line[2].strip()])
        db.commit()
    cur.close()
    db.close()
"""