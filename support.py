# -*- coding: utf-8 -*-
import csv
import httplib
import requests
import re

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


# database get attribute from value
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

total = u"很好【一】1111[2]二二二耳【3】三十三岁3【四死死4】f四efe"
m = kv_parse(total)
for key, value in m.iteritems():
    print key, value


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
