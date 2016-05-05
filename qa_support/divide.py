# -*- coding: utf-8 -*-
import time
import os

class Dictionary:

    def __init__(self, dicnames):
        while os.getcwd().split('/')[-1] != 'graduate':
            os.chdir("../")
        if type(dicnames) is str:
            dicnames = [dicnames]
        self.D = set()
        self.WordMaxLength = 10
        start = time.time()
        for dicname in dicnames:
            dic = open(dicname, 'rb')
            for line in dic:
                if len(line.strip()) != 0:
                    words = line.decode('utf-8').strip().split()
                    for word in words:
                        self.D.add(word)
            dic.close()
        end = time.time()
        # print "Load dictionary time: ", end-start, "S"

    def __del__(self):
        pass

    def existWord(self, word):
        return word in self.D

    def forwardMaxMatch(self, sentence):
        sentence = sentence.strip()
        v = []
        divideIndex = 0
        while True:
            if len(sentence) <= self.WordMaxLength:
                divideIndex = len(sentence)
            else:
                divideIndex = self.WordMaxLength
            while divideIndex is not 0:
                if self.existWord(sentence[0:divideIndex]) or divideIndex == 1:
                    v.append(sentence[0:divideIndex])
                    break
                divideIndex -= 1
            if divideIndex is 0:
                divideIndex += 1
            sentence = sentence[divideIndex:len(sentence)]
            if len(sentence) == 0:
                break
        return v

    def reverseMaxMatch(self, sentence):
        sentence = sentence.strip()
        v = []
        divideIndex = 0
        while True:
            if len(sentence) <= self.WordMaxLength:
               divideIndex = 0
            else:
               divideIndex = len(sentence) - self.WordMaxLength
            while divideIndex != len(sentence):
                if self.existWord(sentence[divideIndex:len(sentence)]) or divideIndex == len(sentence)-1:
                    v.insert(0, sentence[divideIndex:len(sentence)])
                    break
                divideIndex += 1
            if divideIndex == len(sentence):
                divideIndex -= 1
            sentence = sentence[0:divideIndex]
            if len(sentence) == 0:
                break
        return v

    def doubleMaxMatch(self, sentence):
        v1 = self.forwardMaxMatch(sentence)
        v2 = self.reverseMaxMatch(sentence)
        single_sub = 0
        for s in v1:
            if len(s) == 1:
                single_sub += 1
        for s in v2:
            if len(s) == 1:
                single_sub -= 1
        if single_sub > 0:
            return v2
        else:
            return v1

# test
"""
dicnames = ['data/valid_items.txt','data/sample.dic']
dic = Dictionary(dicnames)
with open("data/input.txt", 'rb') as infile:
    for line in infile:
        line = line.strip()
        v = dic.forwardMaxMatch(line.decode('utf-8'))
        print " ".join(v)
        v = dic.reverseMaxMatch(line.decode('utf-8'))
        print " ".join(v)
        v = dic.doubleMaxMatch(line.decode('utf-8'))
        print " ".join(v)
"""