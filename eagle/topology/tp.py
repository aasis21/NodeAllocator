import sys
import os,re
import time
from pathlib import Path

try:
    home = str(Path.home())
except:
    home = os.getenv("HOME")

latency = [[0 for x in range(60)] for y in range(60)] 
count = [[0 for x in range(60)] for y in range(60)] 

def parse_latency(latency):
    try:
        latency = latency.split(" ")
        latency[0] = int( re.findall('\d+', latency[0])[-1] )
        latency[1] = int( re.findall('\d+', latency[1])[-1] )
        latency[2] = int( latency[2])
        return [ latency[0] , latency[1], latency[2] ]
    except:
        return 0
dirs = os.listdir(home + "/.eagle" )
# print(dirs)
for each in dirs:
    db = home + "/.eagle/" + each + "/tphosts.txt.tmp"
    # print(db)
    if os.path.isfile(db):
        file =  open(db,"r")
        while True:
            line = file.readline()
            if not line:
                break
            if( len(line.split(" ")) != 3 or parse_latency(line) == 0 ):
                continue        
            each = parse_latency(line)
            a = int(each[0])
            b = int(each[1])
            l = int(each[2])
            if(l!=50000 and a <=60 and b <=60):
                latency[a-1][b-1] = latency[a-1][b-1] + l
                count[a-1][b-1] = count[a-1][b-1] + 1

# print(latency)
# print(count)

topo = [[40000 for x in range(60)] for y in range(60)] 
for i in range(60):
    for j in range(60):
        if count[i][j] !=0:
            # print(latency[i][j],count[i][j] )
            topo[i][j] = latency[i][j] // count[i][j]
            print( str(i+1) + " " + str(j+1) + " " +  str(topo[i][j]) )

# for i in range(60):
#     print(topo[i])