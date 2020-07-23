import sys
import os,re
import time
from pathlib import Path
import sqlite3 
from statistics import mean 
from matplotlib import pyplot as plt

avg = 5


f = open("bw.txt.t1","r")
data = f.read()
points  = data.strip("\n").split("\n")
for i in range(len(points)):
  points[i] = float(points[i])
p = []
for i in range(0,len(points) - len(points)%avg ,avg):
  p.append(int(float( sum(points[i:i+avg])/avg  )))
p1 = p

    
    
f = open("bw.txt.t2","r")
data = f.read()
points  = data.strip("\n").split("\n")
for i in range(len(points)):
  points[i] = float(points[i])
p = []
for i in range(0,len(points) - len(points)%avg ,avg):
  p.append(int(float( sum(points[i:i+avg])/avg  )))
p2 = p

f = open("bw.txt.t3","r")
data = f.read()
points  = data.strip("\n").split("\n")
for i in range(len(points)):
  points[i] = float(points[i])
p = []
for i in range(0,len(points) - len(points)%avg ,avg):
  p.append(int(float( sum(points[i:i+avg])/avg  )))
p3 = p


l = min(len(p1),len(p2),len(p3))
print(l)

x = [ float(i)/(60/(avg*2)) for i in range(l)]
plt.plot( x, p2[:l], label='Node P - Node Q P2P Bandwidth' )
plt.plot( x, p1[:l], label='Node R - Node S P2P Bandwidth')
plt.plot( x, p3[:l], label='Node T - Node U P2P Bandwidth')

plt.xlabel('Time(hour)')
plt.ylabel('P2P Bandwidth(MBps)')
plt.title("P2P Bandwidth Variation")
plt.ylim(-5,125)
plt.legend()
plt.savefig('p2pbw.jpg')
plt.close()
