#!/bin/python
# -*- coding: UTF-8 -*-
import re
import os, sys
import subprocess
import xlrd, xlwt, xlutils, openpyxl

# rb = xlrd.open_workbook('Book1.xls', formatting_info = True)
# sheet = rb.sheet_by_index(0)
# vals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]
# if int(vals[1][0]) == 1 and int(vals[1][1]) == 3 and int(vals[1][2]) == 2:
#     scheme = vals[1][4]
#     print scheme
#     print 'match'
# else:
#     wb = xlwt.Workbook()
#     ws = wb.add_sheet('test')
#     ws.write (0,0,'sss1')
# wb.save('x1.xls')
wb = openpyxl.load_workbook(filename='Book1.xlsx')
sheet = wb['test']
sheet ['B1'] = 42
wb.save('openpyxl.xlsx')