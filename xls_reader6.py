# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 21:25:39 2015

@author: ichiro_takemura
"""
import pylab as plt
import os

#
def getDirList(path):
    dir_list = []
    for (root, dirs, files) in os.walk(path):
        for dir in dirs:
            dir_list.append(os.path.join(root,dir).replace("\\", "/") )
            print 'hoge'
    return dir_list
    
#def:data_extraction:aa=filepath
def extract(aa):
    data = []
    f = open(aa)
    line = f.readline()
    while line:
        if 'Number' in line:
            line2 = line.strip()
            line2 = line2[23:-7:]
            data.append(line2)
        line = f.readline() 
    f.close
    data.pop(0)
    return data

#def:data_rearrangemnt:zz=datasize
def rear(bb, zz):
    Vb = []
    Va = []
    Ia = []
    Ib = []
    Vab = []
    Iab = []
    r = 0
    if zz == 2:
        for d in bb:
            r +=1
            if r % 4 == 1:
                Vb.append(d)
            elif r % 4 == 2:
                Va.append(d)
            elif r % 4 == 3:
                Ia.append(abs(float(d)))
            elif r % 4 == 0:
                Ib.append(abs(float(d)))
        Vab = [Va, Vb]
        Iab = [Ia, Ib]
    elif zz == 1:
        for d in bb:
            r +=1
            if r % 2 == 1:
                Va.append(d)
            elif r % 2 == 0:
                Ia.append(abs(float(d)))
        Vab = [Va]
        Iab = [Ia]
    return Vab, Iab

#def:plotting:a=graph_number
def plotting(a):
    for x in range (int(a)):
        plt.figure(figsize=(5,5))
        plt.plot(Vdg[x], Idg[x])
        plt.plot(Vlg[x], Ilg[x], 'k--')
        plt.xlim(-5,5)
        plt.ylim(1e-13, 1e-2)
        plt.xticks(range(-5, 6, 1),range(-5, 6, 1))
        plt.yscale('log')
        plt.xlabel('Voltage/ V')
        plt.ylabel('Current Density/ $ cm^2 V^{-1} s^{-1} $')
        graph_title = path_name [root_length:] + 'TEG' + str(x+1)
        plt.title(graph_title)

#device_ab_IV:cc=light-intensity(0:dark,1:1.62,2:5.0):dd=filepathnega:ee,ff=filepath
def IV(cc, dd, ee, ff):
    V = []
    I = []
    Vp = []
    Ip = []
    pathdnega = path_name + '//' + dd [cc]
    pathdposi = path_name + '//' + ee [cc]
    data1 = extract(pathdnega)
    data2 = extract(pathdposi)  
    V, I = rear(data1, ff)
    Vp, Ip = rear(data2, ff)
    for x in range(ff):
        V[x].reverse()
        I[x].reverse()
    for x in range(ff):
        V[x].extend(Vp[x])
        I[x].extend(Ip[x])
    return V, I

def getPaths(list2):
    Path = []
    for x in list2:
        fl = os.listdir(x)
        for y in fl:
            if 'Sweep_Limited' in y:
                Path.append(x)
                break
    return Path

#main
print 'input file path'
path1 = raw_input()

root_length = len(path1)

dlist = []
dlist = getDirList(path1)

Paths = []
Paths = getPaths(dlist)
        
for path in Paths:
    path_name = path
    files = os.listdir(path_name)

    #filename search
    file12nega = []
    file12posi = []
    file34nega = []
    file34posi = []
    file5nega = []
    file5posi = []

    for file in files:
        if 'xls' in file:
            if 'Pad1234' in file:
                if '-' in file[-5]:
                    file12nega.append(file)
                else: 
                    file12posi.append(file)
            elif 'Pad5678' in file:
                if '-' in file[-5]:
                    file34nega.append(file)
                else: 
                    file34posi.append(file)
            elif 'Pad910' in file:
                if '-' in file[-5]:
                    file5nega.append(file)
                else: 
                    file5posi.append(file)
    #I-V
    Vdg = []
    Vlg = []
    Idg = []
    Ilg = []

    Vd12 = []
    Id12 = []
    Vd12, Id12 = IV(0, file12nega, file12posi, 2)
    Vl12 = []
    Il12 = []
    Vl12, Il12 = IV(1, file12nega, file12posi, 2)

    Vd34 = []
    Id34 = []
    Vd34, Id34 = IV(0, file34nega, file34posi, 2)
    Vl34 = []
    Il34 = []
    Vl34, Il34 = IV(1, file34nega, file34posi, 2)

    Vd5 = []
    Id5 = []
    Vd5, Id5 = IV(0, file5nega, file5posi, 1)
    Vl5 = []
    Il5 = []
    Vl5, Il5 = IV(1, file5nega, file5posi, 1)

    Vdg = Vd12 + Vd34 + Vd5
    Vlg = Vl12 + Vl34 + Vl5
    Idg = Id12 + Id34 + Id5
    Ilg = Il12 + Il34 + Il5

    #plotting
    plotting(1)
