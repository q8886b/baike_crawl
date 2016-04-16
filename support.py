# -*- coding: utf-8 -*-
import csv
import httplib
import requests

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
