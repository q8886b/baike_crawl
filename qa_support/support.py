# -*- coding: utf-8 -*-
import csv
import httplib
import requests
import re
import MySQLdb
import sys
import os

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
with open('../data/medicine.csv', 'rb') as infile, open('../data/medicine.url', 'wb') as outfile:
    url_prefix = "http://www.baike.baidu.com/item/"
    spamreader = csv.reader(infile, delimiter=',')
    for row in spamreader:
        outfile.write(url_prefix + row[0] + "\n")
"""

# from clean csv file to item dictionary
"""
with open('../data/medicine.csv', 'rb') as infile, open('../data/item.dic', 'wb') as outfile:
    spamreader = csv.reader(infile, delimiter=',')
    for row in spamreader:
        outfile.write(row[0] + "\n")
"""

# count valid url from baike.com

"""
with open('../data/item.dic', 'rb') as infile:
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
with open('../data/attribute_key.txt', 'rb') as infile:
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


with open("../data/kv_in_value.txt", 'rb') as infile, open("../data/kv_in_value_output.csv", 'wb') as outfile, \
        open("../data/attribute_key.txt", 'rb') as keyfile:
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

with open("../data/kv_in_value_output.csv", 'rb') as infile:
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

# export to table medicine_simple, create table attribute_set
# attribute sample: 1简介　2功用　3制备　4用法　5别名　６性味　７来源　８鉴定　９生态环境  10成分
#                   11归经 12培育 13毒性 14禁忌 15文化

"""
db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='graduate', charset='utf8')
cur_r = db.cursor()
cur_w = db.cursor()
ATTR_NUM = 15
attrs = [set() for x in xrange(ATTR_NUM)]
with open("../data/attribute_key.txt", 'rb') as infile:
    for i in range(15):
        line = infile.readline().decode('utf-8')
        for word in line.split():
            attrs[i].add(word)
attrs_sample = [u'简介', u'功用', u'制备', u'用法', u'别名', u'性味', u'来源', u'鉴定', u'生态环境', u'成分',
                u'归经', u'培育', u'毒性', u'禁忌', u'文化']
black_list = [u'方剂名称']
write_list = [u'处方来源', u'【处方来源】']
def find_attr(input):
    if input in black_list:
        return set()
    idx_found = set()
    for idx in range(ATTR_NUM):
        for a in attrs[idx]:
            if input.find(a) != -1:
                if (input == a) or input in write_list:
                    idx_found.clear()
                    idx_found.add(idx)
                    return idx_found
                else:
                    idx_found.add(idx)
                    break
    if 0 in idx_found:
        if len(idx_found) != 1:
            idx_found.remove(0)
    return idx_found

sql_r = "select * from medicine"
cur_r.execute(sql_r)
sql_w = "insert into medicine_simple values(%s, %s, %s)"
for row in cur_r:
    src = find_attr(row[1])
    for idx in src:
        cur_w.execute(sql_w, [row[0].encode('utf-8'), attrs_sample[idx].encode('utf-8'), row[2].encode('utf-8')])
        db.commit()

sql_w = "insert into attributes values(%s, %s)"
for idx in range(0, ATTR_NUM):
    for attr in attrs[idx]:
        cur_w.execute(sql_w, [attrs_sample[idx].encode('utf-8'), attr.encode('utf-8')])
        db.commit()
cur_r.close()
cur_w.close()
db.close()
"""

# create synonym
"""
with open("../data/item_synonym.txt", 'wb') as outfile, open('../data/attribute_key.txt', 'rb') as keyfile:
    keys = set()
    for line in keyfile:
        line = line.decode('utf-8')
        sl = line.strip().split()
        for s in sl:
            keys.add(s)

    db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='graduate', charset='utf8')
    cur = db.cursor()
    #from value
    sql = "select item, value from graduate.medicine where value like %s"
    cur.execute(sql, ['%别名%'])
    terminals = [u'。', u'；', u'学名', u'拉丁', u'中文', u'汉语', u'英文', u'是']
    for key in keys:
        terminals.append(key)
    terminals.remove(u'别名')
    for row in cur:
        begin = row[1].find(u'别名')
        end = 0xfffffff
        for s in terminals:
            if end > row[1].find(s, begin) and row[1].find(s, begin) != -1:
                end = row[1].find(s, begin)
        if end == -1:
            result = row[1][begin:].encode('utf-8').strip()
        else:
            result = row[1][begin:end].encode('utf-8').strip()
        result = result[6:].decode('utf-8')
        result = re.sub(u'《.*?》|（.*?）(.*?)', ' ', result)
        print result
        results = re.split(u" |，|、|,|：|:|《|（|\(f|》|）|\)", result)
        result = u" ".join(results).encode('utf-8')
        outfile.write(row[0].encode('utf-8') + " 　　" + result + '\n')
    #from attribute
    sql = "select item, value from graduate.medicine where attribute = '别名'"
    cur.execute(sql)
    for row in cur:
        result = row[1].encode('utf-8').strip().decode('utf-8')
        result = re.sub(u'《.*?》|（.*?）(.*?)', ' ', result)
        print result
        results = re.split(u" |，|、|,|：|:|《|（|\(f|》|）|\)", result)
        result = u" ".join(results).encode('utf-8')
        outfile.write(row[0].encode('utf-8') + " 　　" + result + '\n')
"""

#create synonym in mysql
"""
with open("data/item_synonym.txt", 'rb') as infile:
    items = dict()
    blacks = set()
    sa = set()
    for line in infile:
        ss = line.decode('utf-8').split()
        if len(ss) <= 1:
            continue
        else:
            if items.has_key(ss[0]) is False:
                items[ss[0]] = set()
            for idx in range(1, len(ss)):
                if ss[idx] in sa:
                    blacks.add(ss[idx])
                if ss[idx] not in blacks:
                    items[ss[0]].add(ss[idx])
                    sa.add(ss[idx])

    db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='graduate', charset='utf8')
    cur = db.cursor()
    sql = "insert into items values(%s, %s)";
    for k, v in items.iteritems():
        for sym in v:
            cur.execute(sql, [k.encode('utf-8'), sym.encode('utf-8')])
            db.commit()
    db.close()
"""

#tf-idf dictionary to normal dictionary
"""
with open("data/attribute.dic", 'rb') as infile, open("data/exchange.txt", 'wb') as outfile:
    limit = 1e-10
    words = []
    for line in infile:
        if len(line.strip()) == 0:
            continue
        ss = line.decode('utf-8').strip().split()
        if float(ss[1]) > limit:
            words.append(ss[0])
    for word in words:
        outfile.write(word.encode('utf-8') + '\n')
"""

#create dic from 15 file
"""
db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='graduate', charset='utf8')
cur = db.cursor()
sql = "select value from medicine_simple where attribute = %s into outfile %s fields terminated by ',' "  \
      "enclosed by '\"' lines terminated by '\n'"
attrs_sample = [u'简介', u'功用', u'制备', u'用法', u'别名', u'性味', u'来源', u'鉴定', u'生态环境', u'成分',
                u'归经', u'培育', u'毒性', u'禁忌', u'文化']
i = 0
for attr in attrs_sample:
    i += 1
    cur.execute(sql, [attr.encode('utf-8'), str(i)+".txt"])
"""

#1-15 encoding transfer
"""
for x in range(1,16):
    filename = str(x)
    outname = str(x) + ".txt"
    with open("data/" + filename, 'rb') as infile, open("data/" + outname, 'wb') as outfile:
        for line in infile:
            line = line.decode('utf-8').encode('gb18030')
            outfile.write(line)
"""

# known url and valid url append to known.url and valid.url
"""
with open("data/exchange.txt", 'rb') as infile, open("data/known.url", 'a') as outfile1, \
        open("data/valid.url", 'a') as outfile2, open("data/baike.url", 'wb') as outfile3:
    for line in infile:
        if line.find("known") == -1:
            outfile2.write(line[5:])
            outfile3.write(line[5:])
        else:
            outfile1.write(line[11:])
"""

# see different between two item file

"""
with open("data/valid_items.txt", 'rb') as file1, open("data/item_expand.txt", 'rb') as file2:
    s1 = set([line.strip() for line in file1])
    s2 = set([line.strip() for line in file2])
    for item in s1:
        if item not in s2:
            print "invalid:", item
    for item in s2:
        if item not in s1:
            print "new:", item
"""