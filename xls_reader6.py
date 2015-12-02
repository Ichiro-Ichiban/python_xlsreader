# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 21:25:39 2015

@author: ichiro_takemura
"""
import pylab as plt
import os
import numpy as np

#
def getDirList(path):
    dir_list = []
    for (root, dirs, files) in os.walk(path):
        for dir in dirs:
            dir_list.append(os.path.join(root,dir).replace("\\", "/") )
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
def rear(bb, data_size):
    Vb = []
    Va = []
    Ia = []
    Ib = []
    Vab = []
    Iab = []
    r = 0
    if data_size == 2:
        for d in bb:
            r +=1
            if r % 4 == 1:
                Vb.append(float(d))
            elif r % 4 == 2:
                Va.append(float(d))
            elif r % 4 == 3:
                Ia.append(abs(float(d)))
            elif r % 4 == 0:
                Ib.append(abs(float(d)))
        Vab = [Va, Vb]
        Iab = [Ia, Ib]
    elif data_size == 1:
        for d in bb:
            r +=1
            if r % 2 == 1:
                Va.append(float(d))
            elif r % 2 == 0:
                Ia.append(abs(float(d)))
        Vab = [Va]
        Iab = [Ia]
    return Vab, Iab

def plotMedian(Vd, Id, Vl, Il, path_name):
    plt.figure(figsize=(5,5))
    plt.plot(Vd, Id)
    plt.plot(Vl, Il, 'k--')
    plt.xlim(-5,5)
    plt.ylim(1e-13, 1e-2)
    plt.xticks(range(-5, 6, 1),range(-5, 6, 1))
    plt.yscale('log')
    plt.xlabel('Voltage/ V')
    plt.ylabel('Current Density/ $ cm^2 V^{-1} s^{-1} $')
    graph_title = path_name [root_length:]
    plt.title(graph_title)

"""
def plotAll(a, Vd, Id, Vl, Il, path_name):
    for x in range(a):
        print x
        plt.figure()
        plt.subplot(3,2,x+1)
        plt.plot(Vd[x], Id[x])
        plt.plot(Vl[x], Il[x], 'k--')
        plt.xlim(-5,5)
        plt.ylim(1e-13, 1e-2)
        plt.xticks(range(-5, 6, 1),range(-5, 6, 1))
        plt.yscale('log')
        plt.xlabel('Voltage/ V')
        plt.ylabel('Current Density/ $ cm^2 V^{-1} s^{-1} $')
        graph_title = path_name [root_length:] + 'TEG_' + x
        plt.title(graph_title)
        plt.tight_layout()
"""

#device_ab_IV:li=light-intensity(0:dark,1:1.62,2:5.0):dd, ee=filepathnega:nd=number of device
def getIV(li, dd, ee, nd, path_name):
    V = []
    I = []
    Vp = []
    Ip = []
    path_nega = path_name + '//' + dd [li]
    path_posi = path_name + '//' + ee [li]
    data_n = extract(path_nega)
    data_p = extract(path_posi)  
    V, I = rear(data_n, nd)
    Vp, Ip = rear(data_p, nd)
    for x in range(nd):
        V[x].reverse()
        I[x].reverse()
    for x in range(nd):
        V[x].extend(Vp[x])
        I[x].extend(Ip[x])
    return V, I

def getPath(list2):
    Path = []
    for x in list2:
        fl = os.listdir(x)
        for y in fl:
            if 'Sweep_Limited' in y:
                Path.append(x)
                break
    return Path

def getFileName(files2):
    f12n = []
    f12p = []
    f34n = []
    f34p = []
    f5n = []
    f5p = []

    for file in files2:
        if 'xls' in file:
            if 'Pad1234' in file:
                if '-' in file[-5]:
                    f12n.append(file)
                else: 
                    f12p.append(file)
            elif 'Pad5678' in file:
                if '-' in file[-5]:
                    f34n.append(file)
                else: 
                    f34p.append(file)
            elif 'Pad910' in file:
                if '-' in file[-5]:
                    f5n.append(file)
                else: 
                    f5p.append(file)
    return f12n, f12p, f34n, f34p, f5n, f5p

def getMedian(data):
    d_median = []
    for y in range(len(data[0])):
        d_add = []
        for x in range (5):
            d_add.append(data[x, y])
        d_median.append(np.median(d_add))
    return d_median

#main
print 'input file path'
root_path = raw_input()

root_length = len(root_path)

list = []
dlist = getDirList(root_path)

file_path = []
file_path = getPath(dlist)

for path in file_path:
    files = os.listdir(path)

    file12nega = []
    file12posi = []
    file34nega = []
    file34posi = []
    file5nega = []
    file5posi = []
    
    file12nega, file12posi, file34nega, file34posi, file5nega, file5posi = getFileName(files)

    #I-V
    Vd12 = []
    Vd34 = []
    Vd5 = []

    Id12 = []
    Id34 = []
    Id5 = []

    Vl12 = []
    Vl34 = []
    Vl5 = []

    Il12 = []
    Il34 = []
    Il5 = []
  
    Vd12, Id12 = getIV(0, file12nega, file12posi, 2, path)
    Vd34, Id34 = getIV(0, file34nega, file34posi, 2, path)
    Vd5, Id5 = getIV(0, file5nega, file5posi, 1, path)

    Vl12, Il12 = getIV(1, file12nega, file12posi, 2, path)
    Vl34, Il34 = getIV(1, file34nega, file34posi, 2, path)
    Vl5, Il5 = getIV(1, file5nega, file5posi, 1, path)

    Vdg = []
    Vlg = []
    Idg = []
    Ilg = []

    Vdg = Vd12 + Vd34 + Vd5
    Idg = Id12 + Id34 + Id5
    Vlg = Vl12 + Vl34 + Vl5
    Ilg = Il12 + Il34 + Il5

    Vd_array = np.array(Vdg)
    Vl_array = np.array(Vlg)
    Id_array = np.array(Idg)
    Il_array = np.array(Ilg)

    Vdm = []
    Vlm = []
    Idm = []
    Ilm = []
    
    Vdm = getMedian(Vd_array)
    Vlm = getMedian(Vl_array)
    Idm = getMedian(Id_array)
    Ilm = getMedian(Il_array)

    #plotting
    plotMedian(Vdm, Idm, Vlm, Ilm, path)
    #plotAll(1, Vdg, Idg, Vlg, Ilg, path)    