# -*- coding: utf-8 -*-
import csv

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

# from csv file to url
with open('medicine.csv', 'rb') as infile, open('medicine.url', 'wb') as outfile:
    url_prefix = "http://www.baike.baidu.com/item/"
    spamreader = csv.reader(infile, delimiter=',')
    s = set([])
    for row in spamreader:
        outfile.write(url_prefix + row[0] + "\n")




