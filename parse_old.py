#!/bin/python
# -*- coding: UTF-8 -*-
import re

f = open('pattern2', 'r')
text = f.read()
tests = []
tests = re.findall('\*(.*?)\n', text)

for i in xrange(len(tests)):
    test1 = tests[i].split(' ')
    if test1[1] == 'lrc':
        mod = 'lrc'
        if test1[2][:6] == 'scheme':
            scheme = test1[2][7:]
        if test1[2][:6] == 'groups':
            groups = int(test1[2][7:])
            length = int(test1[3][7:])

            # print groups
            # print length

            # try:
            #     if test1[4][:8] == 'global_s':
            #         global_s = test1[4][9:]
            #         # continue
            #                 # print global_s
            # except IndexError:
            #     global_s = 1

    elif test1[1] == 'raid6':
        mod = 'raid6'
    print test1
    # print test1[2]
    # print tests[i]
    # print mod
    # print scheme
    # print groups
    # print length
    # print groups
f.close()
# print tests