# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 21:25:39 2015

@author: ichiro_takemura
"""
import pylab as plt

r = 0
f1 = open('/Users/ichiro_takemura/Documents/test/Pad1234_nega_0uW.xls')
line = f1.readline()

V3 = []
V1 = []
I1 = []
I3 = []
data = []

while line:
    if 'Number' in line:
        line = line.strip()
        line = line[23:-7:]
        data.append(line)
    line = f1.readline()

f1.close

data.pop(0)

for d in data:
    r +=1
    if r % 4 == 1:
        V3.append(d)
    elif r % 4 == 2:
        V1.append(d)
    elif r % 4 == 3:
        I1.append(abs(float(d)))
    elif r % 4 == 0:
        I3.append(abs(float(d)))

V3.reverse()
V1.reverse()
I1.reverse()
I3.reverse()

f2 = open('/Users/ichiro_takemura/Documents/test/Pad1234_posi_0uW.xls')
line2 = f2.readline()

data2 = []

while line2:
    if 'Number' in line2:
        line2 = line2.strip()
        line2 = line2[23:-7:]
        data2.append(line2)
    line2 = f2.readline()

f2.close

data2.pop(0)

r = 0

for d in data2:
    r +=1
    if r % 4 == 1:
        V3.append(d)
    elif r % 4 == 2:
        V1.append(d)
    elif r % 4 == 3:
        I1.append(abs(float(d)))
    elif r % 4 == 0:
        I3.append(abs(float(d)))

plt.plot(V1, I1)
plt.plot(V3, I3)
plt.yscale('log')