# coding=utf-8
from Tkinter import *


similar_list = []
def add_column(value):
    similar_list.append([value])
def add_exist(num, value):
    similar_list[num].append(value)

blacks = set()
whites = set()

done_list = set()

def word_filter(word):
    for black in blacks:
        if word.decode('utf-8').find(black) != -1:
            return ""
    for white in whites:
        if word.decode('utf-8').find(white) != -1:
            return ""
    for done in done_list:
        if done == word:
            return ""
    done_list.add(word)
    return word

def b_add(idx):
    text = v.get()
    add_exist(idx, text)
    ts[idx].insert(END, text)
    f_read.next()

def b_new():
    text = v.get()
    add_column(text)
    idx = len(similar_list) - 1
    b = Button(win,text=str(idx))
    bs.append(b)
    row = (idx / 10) * 2
    column = idx % 10
    bs[idx].grid(row=3+row, column=column)
    bs[idx].configure(command=lambda:b_add(idx))
    t = Listbox(win, height=3)
    ts.append(t)
    for word in similar_list[idx]:
        ts[-1].insert(END, word)
        ts[-1].grid(row=4+row, column=column)
    f_read.next()

def but_save():
    with open('data/exchange.txt', 'wb') as outfile:
        for similars in similar_list:
            for word in similars:
                print word
                outfile.write(word.encode('utf-8') + " ")
            outfile.write("\n")
        for black in blacks:
            outfile.write(black.encode('utf-8') + " ")
        outfile.write("\n")
        for white in whites:
            outfile.write(white.encode('utf-8') + " ")
        outfile.write("\n")
        outfile.close()


def but_white():
    text = v.get()
    if text not in whites:
        whites.add(text)
        l_white.insert(END, text)
def but_black():
    text = v.get()
    if text not in blacks:
        blacks.add(text)
        l_black.insert(END, text)

def read_next():
    with open('data/attribute.csv', 'rb') as infile:
        n = 0
        for word in infile:
            n+=1
            if n % 10 == 0:
                print n
            if word_filter(word.strip()) == "":
                continue
            v.set(word.strip())
            yield 1
    with open('data/key.txt', 'wb') as outfile:
        for similars in similar_list:
            for word in similars:
                print word
                outfile.write(word.encode('utf-8') + " ")
            outfile.write("\n")
        outfile.close()


win=Tk()
f_read = read_next()
bs = []
ts = []
b0 = Button(win,text="New")
b_next = Button(win, text="next")
b_save = Button(win, text="save")
v = StringVar()
e = Entry(win, textvariable=v)
l_white = Listbox(win, height=3)
l_black = Listbox(win, height=3)
b_white = Button(win, text="white")
b_black = Button(win, text="black")

#layout
l_white.grid(row=0, column=0)
b_white.grid(row=0, column=1)
l_black.grid(row=1, column=0)
b_black.grid(row=1, column=1)
e.grid(row=2, column=0)
b0.grid(row=2, column=1)
b_next.grid(row=2, column=2)
b_save.grid(row=2, column=3)

#event
b0.configure(command=b_new)
b_white.configure(command=but_white)
b_black.configure(command=but_black)
b_next.configure(command=lambda:f_read.next())
b_save.configure(command=but_save)

win.mainloop()

