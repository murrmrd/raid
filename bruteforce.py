#!/bin/python
# -*- coding: UTF-8 -*-
import threading
import subprocess
import time
# command1 = "./main 1 1 > tmp.res ; cat tmp.res | grep G | sed -e 's/^.*[\t]//g; s/[ \t]//g; q' ; rm -f tmp.res; sleep 10"

command1 ="cd /home/murrm/practice/PyramidalBruteforce-random-shuffle; ./main 1 1 > tmp.res ; cat tmp.res | grep G | sed -e 's/^.*[\t]//g; s/[ \t]//g; q' ; rm -f tmp.res ; "
process1 = subprocess.Popen(command1, stdout=subprocess.PIPE, shell=True)
# out,err = process.communicate()

# t = threading.Timer(10.0, go)
# t.start()

out = process1.stdout.read()
# time.sleep(10)
print out

command2 = "ps aux | grep './main 1 1' | grep R | awk '{print $2}' ;"
process2 = subprocess.Popen(command2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
number = int(process2.stdout.read())+1
print number


# command3 = "kill -INT %s" % (int(number))
# process = subprocess.call(command3, shell=True)
# print out
# print output
