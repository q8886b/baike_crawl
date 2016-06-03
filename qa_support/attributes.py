# coding=utf-8
import MySQLdb
import os
import sys
import divide

class TFDictionary:
    def __init__(self, dicname):
        while os.getcwd().split('/')[-1] != 'graduate':
            os.chdir("../")
        item_dic = divide.Dictionary(['data/valid_items.txt'])
        dic = open(dicname, 'rb')
        self.D = dict()
        for line in dic:
            words = line.decode('utf-8').strip().split()
            if item_dic.existWord(words[0]) is False:
                self.D[words[0]] = float(words[1])
        dic.close()
    def cal(self, words):
        tf_value = 0.0
        for word in words:
            if (self.D.has_key(word)):
                tf_value += self.D[word]
        return tf_value
    def exist(self, word):
        return self.D.has_key(word)


def find_attr(words):
    #find keyword from table attribute
    db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='graduate', charset='utf8')
    cur = db.cursor()
    sql = 'select attribute from attributes where synonym = %s'
    attrs = set()
    for word in words:
        cur.execute(sql, [word.encode('utf-8')])
        for row in cur:
            # print word.encode('utf-8'), row[0].encode('utf-8')
            attrs.add(row[0])
    #if no attribute keyword found
    #attrs_sample = [u'简介', u'功用', u'制备', u'用法', u'别名', u'性味', u'来源', u'鉴定', u'生态环境', u'成分',
    #                u'归经', u'培育', u'毒性', u'禁忌', u'文化']
    attrs_sample = [u'功用', u'制备', u'用法', u'别名', u'性味', u'来源', u'鉴定', u'生态环境', u'成分',
                    u'归经', u'培育', u'毒性', u'禁忌']
    while os.getcwd().split('/')[-1] != 'graduate':
        os.chdir("../")
    if len(attrs) == 0:
        values = []
        for i in range(1, 14):
            filename = "data/" + str(i) + ".dic"
            tfdic = TFDictionary(filename)
            values.append(tfdic.cal(words))
        max_index = values.index(max(values))
        attrs.add(attrs_sample[max_index])
        values_copy = values
        # print max(values)
        for i in range(0,13):
            values_copy[i] = str(values_copy[i])
        # print " ".join(values_copy)

    return attrs

