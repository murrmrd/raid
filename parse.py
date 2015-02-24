#!/bin/python
# -*- coding: UTF-8 -*-
import re
import os, sys
import subprocess
import xlrd, xlwt, xlutils

f = open('pattern2', 'r')
text = f.read()
tests = []
tests = re.findall('\*(.*?)\n', text)

for i in xrange(len(tests)):
    test1 = tests[i].split(' ')
    # for j in xrange(len(test1)-1):
    #      if j < len(test1):
    if test1[1] == 'lrc':
        mod = 'lrc'
        if test1[2][:6] == 'scheme':
            scheme = test1[2][7:]
            table = open('TABLE1','a')
            table.write('0  insane %s recover 1 %s %s \n' % (mod, int(test1[0]), scheme))
            table.close()
        if test1[2][:6] == 'groups':
            groups = int(test1[2][7:])
            length = int(test1[3][7:])
            if len(test1) > 4:
                global_s = int(test1[4][9:])
            else:
                global_s = 1
            defines = open('defines','a')
            defines.write('#define disks_count %s\n#define groups_count %s\n#define group_len %s\n' % (int(test1[0]),groups,length))

            # try:
            #     if test1[4][:8] == 'global_s':
            #         global_s = test1[4][9:]
            #         # continue
            #                 # print global_s
            # except IndexError:
            #     global_s = 1

    elif test1[1] == 'raid6':
        mod = 'raid6'
    command = 'echo 123 >> echo1.txt'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output,error = process.communicate()
    print test1
print tests
f.close()