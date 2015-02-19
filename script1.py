# -*- coding: UTF-8 -*-
import re
f = open('pattern', 'r')
text = f.read()
result = re.findall('{(.*?)}', text)
disks = re.findall('count_disks=(.*?) ', text)
sizes = re.findall('sizes=(.*?)\n', text)
partitions = result[0].split(' ')
sequence = re.findall('scheme (.*?)\n', text)
# print sequence[0]
# partitions = int(result[0].count('dev'))
if len(partitions) < int(disks[0]):
    print 'Error, partitions < disks'
    exit()
parts = []
for i in xrange(int(disks[0])):
    parts.append(partitions[i])
b = ' '.join(parts)
c = sizes[0].split(' ')
size_disk = int(result[1][:-1])
byte = (result[1][-1])
if byte == 'G'or byte == 'g':
    size_block = int(disks[0])*2*1024*1024*size_disk
if byte == 'M' or byte == 'm':
    size_block = int(disks[0])*2*1024*size_disk
if byte == 'K' or byte == 'k':
    size_block = int(disks[0])*2*size_disk
mod = re.findall('module=(.*?) ', text)
table = open('table', 'a')
for i in xrange(len(c)):
    table.write('0 %s insane %s %s %s recover 1 %s \n' % (size_block, mod[0], int(disks[0]), int(c[i]), b))
table.close()
# print(result)
# массив из данных в скобках {}
# print size_disk
# размер одного диска
# print byte
# еденицы измерения диска-G,M,K
# print disks[0]
# количество дисков
# print size_block
# размер всего устройства=2*1024*N...
# print mod[0]
# используемый модуль(lrc,raid 6,...)
# print sizes
# массив с размерами блоков
# print partitions
# массив с разделами
# print b
# используемые разделы
# print c
# массив с используемыми размерами блоков

# size_block=int(disks[0])*2
# for line in f:
#     print line
#     result = re.findall

# disks = file.readline().strip()
# print file.readlines()
# for line in file:
#     print line
# data = re.split(r'\n{2,}',file )
# print data
