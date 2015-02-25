#!/bin/python
# -*- coding: UTF-8 -*-
schemes = 'schemes.csv'
columns = {'groups':0, 'length':1,'disks':2,'global_s':3,'scheme':4}

def dict2list(dct):
    lst = ['']*len(dct)

    for i in dct.items():
        lst[columns[i[0]]] = i[1]

    return lst

def add_scheme(dct):
    lst = dict2list(dct)
    schm = ','.join(str(i) for i in lst) + '\n'

    with open(schemes, "a") as f:
        f.write(schm)

    return 0
        
def search_scheme(params):
    f = open(schemes)
    
    for line in f:
        array = line.split(',')
        match = True
        for j in params.items():
            try:
                pattern = int(array[columns[j[0]]])
            except:
                pattern = 0
            if (pattern != j[1]):
                match = False

        if match:
            return array[columns['scheme']].strip()
        
    return 0

params = {'groups':0, 'length':4,'disks':11,'global_s':1}
print search_scheme(params)
add_scheme(params)



# dict={'2':0,'4':1,'11':2,'1':3}
# print search_scheme(dict)

#schm = ['groups':2,'length':4,'disks':11,'global_s':1,scheme:'s2s1e122g211']
#add_scheme(schm)
#dict2list(columns)
