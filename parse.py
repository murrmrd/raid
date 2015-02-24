#!/bin/python
# -*- coding: UTF-8 -*-
import re
import os, sys
import subprocess
import xlrd, xlwt, xlutils
# f = open('pattern2', 'r')
# text = f.read()
def read_section(section):
    lst = open('pattern2','r').readlines()
    i = 0
    result = []
    for line in lst:
        if '[' in line:
            i += 1
        if i == section:
            if (line[0] != '#') and (line.strip() != '') and (line[0] != '['):
                result.append(line.strip())
    return result # не разобралась как передавать название секции а не номер,не работет у меня почему то
                  #по номеру все отлично

devices = read_section(1)
volume = read_section(2)
sizes = read_section(3)
tests = read_section(4)
# devices = re.findall('\[devices\]\n(.*?)\n', text)
# volume = re.findall('\[volume\]\n(.*?)\n', text)
# sizes = re.findall('\[block_sizes\]\n(.*?)\n', text)
partitions = devices[0].split(' ')
size_disk = int(volume[0][:-1])
byte = (volume[0][-1])
# tests = []
# tests = re.findall('\*(.*?)\n', text)

for i in xrange(len(tests)):
    test1 = tests[i].split(' ')

    if len(partitions) < int(test1[0]):
        print 'Error, partitions < disks'
        exit()

    if len(test1) > 2:
        if test1[2][:6] == 'scheme':
            get_scheme = test1[2][7:] #скопировала сюда же get_constants, так удобнее

            def defines(scheme):
                sd = scheme.count('1') - 1
                ss = scheme.count('s') + scheme.count('S')
                eb = scheme.count('e') + scheme.count('E')
                gs = scheme.count('g') + scheme.count('G')

                dfns = []

                dfns.append('#define SUBSTRIPES ' + str(ss) + '\n')
                dfns.append('#define SUBSTRIPE_DATA ' + str(sd) + '\n')
                dfns.append('#define E_BLOCKS ' + str(eb) + '\n')
                dfns.append('#define GLOBAL_S ' + str(gs) + '\n')

                return dfns

                # Вспомогательная функция вывода массива в годном для C виде
            def print_array(array):
                st = '{'

                for i in array:
                    st += str(i)
                    st += ', '

                st = st[:-2] + '};\n' # Стираем последнюю запятую и добавляем фигурную скобку
                return st

                # Эта функция переводит введенную схему в
                # схему, понятную сишному модулю.

            def get_hex_scheme(scheme):
                i = 0
                array = []

                # Здесь такой дурной цикл по той причине, что в локальном
                # синдроме требуется обрабатывать два символа за раз
                while i < len(scheme):
                    if scheme[i].isdigit():                                 # Блок данных
                        array.append(hex(int(scheme[i]) - 1))
                    else:
                        if ((scheme[i] == 's') or (scheme[i] == 'S')):      # Локальный синдром
                            array.append(hex(191 + int(scheme[i+1])))
                            i += 1
                        elif ((scheme[i] == 'e') or (scheme[i] == 'E')):    # Empty-block
                            array.append(hex(0xee))
                        else:                                               # Глобальный синдром
                            array.append(hex(0xff))
                    i += 1
                return array

                # Следующие 5 функций нужны специально для того,
                # чтобы формировать некоторые переменные для файла.

            def get_data_scheme(hex_scheme):
                array = []

                for i in hex_scheme:
                    fs = i[2]
                    if ((fs != 'c') and (fs != 'e') and (fs != 'f')):
                        array.append(i)
                return array

            def get_ls_places(hex_scheme):
                i = 0
                array = []
                while i < len(hex_scheme):
                    if (hex_scheme[i][2] == 'c'):
                        array.append(i)
                    i += 1
                return array

            def get_gs(hex_scheme):
                i = 0
                array = []
                while i < len(hex_scheme):
                    if(hex_scheme[i][2] == 'f'):
                        array.append(i)
                    i += 1
                return array

            def ordered_offset(hex_scheme):
                array = []
                array[0:0] = (get_ls_places(hex_scheme))    # Сперва получим локальные синдромы
                array[1:1] = (get_gs(hex_scheme))           # Потом глобальные
                array.append(hex_scheme.index(hex(0xee)))   # А потом empty-block

                array.sort()
                return array

            def get_ldb(hex_scheme):
                i = len(hex_scheme) - 1
                while i >= 0:
                    fs = hex_scheme[i][2]
                    if ((fs != 'c') and (fs != 'e') and (fs !='f')):
                        break;
                    i -= 1
                return i



                # Эта функция формирует основной массив строк файла lrc_config.c, ее можно не трогать
            def constants(scheme):
                cnstns = []
                cnstns.append('\n')
                cnstns.append('const unsigned char lrc_scheme[(SUBSTRIPE_DATA + 1) * SUBSTRIPES + E_BLOCKS + GLOBAL_S] =\n')
                hex_scheme = get_hex_scheme(scheme)
                cnstns.append(print_array(hex_scheme))
                cnstns.append('\n')

                cnstns.append('// it is just lrc_scheme without 0xee, 0xff and 0xcN\n')
                cnstns.append('const unsigned char lrc_data[SUBSTRIPE_DATA * SUBSTRIPES] =\n')
                data_scheme = get_data_scheme(hex_scheme)
                cnstns.append(print_array(data_scheme))
                cnstns.append('\n')

                cnstns.append('// it is place of global syndrome\n')
                gs_array = get_gs(hex_scheme)
                cnstns.append('const int lrc_gs[GLOBAL_S] = ')
                cnstns.append(print_array(gs_array))
                cnstns.append('\n')

                cnstns.append('// places of all local syndromes\n')
                cnstns.append('const int lrc_ls[SUBSTRIPES] = ')
                ls = get_ls_places(hex_scheme)
                cnstns.append(print_array(ls))

                cnstns.append('// empty place\n')
                cnstns.append('const int lrc_eb = ' + str(hex_scheme.index(hex(0xee))) + ';\n')

                cnstns.append('// not-data blocks, ordered by increasing\n')
                cnstns.append('const int lrc_offset[SUBSTRIPES + E_BLOCKS + GLOBAL_S] = ')
                oo = ordered_offset(hex_scheme)
                cnstns.append(print_array(oo))

                cnstns.append('// number of the last data block\n')
                cnstns.append('const int lrc_ldb = ' + str(get_ldb(hex_scheme)) + ';\n')
                cnstns.append('\n')

                return cnstns

            def make_file(scheme):
                new_info = defines(scheme)
                new_info += constants(scheme)
                with open('lrc_config.c', 'w') as file:
                    file.writelines(new_info)

            def main():
                scheme = get_scheme
                make_file(scheme)

            if __name__ == '__main__':
                main()

        if test1[2][:6] == 'groups':
            groups = int(test1[2][7:])
            length = int(test1[3][7:])
            if len(test1) > 4:
                global_s = int(test1[4][9:])
            else:
                global_s = 1

            with open('defines','w') as defns:
                defns.write('#define disks_count %s\n#define groups_count %s\n#define group_len %s\n' % (int(test1[0]),groups,length))

            #тут искалка и поиск/запись в таблицу
    parts=[]
    for j in xrange(int(test1[0])):
        parts.append(partitions[j])
        b = ' '.join(parts)
        c = sizes[0].split(' ')
        if byte == 'G'or byte == 'g':
            size_block = int(test1[0])*2*1024*1024*size_disk
        if byte == 'M' or byte == 'm':
            size_block = int(test1[0])*2*1024*size_disk
        if byte == 'K' or byte == 'k':
            size_block = int(test1[0])*2*size_disk

    with open('TABLE1','a') as table:
        for k in xrange(len(c)):
            table.write('0 %s insane %s %s %s recover 1 %s  \n' % (size_block, test1[1], int(test1[0]), int(c[k]),b ))#+размер блоков и тд

    command = 'echo 123 >> echo1.txt' #тут будут bash скрипты
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output,error = process.communicate()
    # print test1
# print tests
# f.close()