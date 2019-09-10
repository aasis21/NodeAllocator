import sys
import os,re
import time
from pathlib import Path
import sqlite3 
from statistics import mean 
from matplotlib import pyplot as plt



try:
    home = str(Path.home())
except:
    home = os.getenv("HOME")

def read_node_data_from_db(db_file):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    node_sql = """
    SELECT * FROM node_monitor 

    """
    rows = []
    try:
        cur.execute(node_sql)
        rows = cur.fetchall()
        print(len(rows))
    except:
        print(" No data ")
        return None

    i = 0
    steps = 500
    avg_data = []
    while( i+steps < len(rows)):
        # print("\n"+str(i) + ":" + str(i+steps))
        slice = rows[i:i+steps]
        zipped = zip(*slice)
        avg_val = []
        for each in list(zipped)[7:]:
            avg_val.append( mean(each))
        
        load_avg = ( 0.5 * (avg_val[0]) + 0.3 * (avg_val[1]) + 0.2 * (avg_val[2])) % 25
        bd_avg = ( 0.5 * (avg_val[3]) + 0.3 * (avg_val[4]) + 0.2 * (avg_val[5]) ) / 1000000
        util_avg = 0.5 * (avg_val[6]) + 0.3 * (avg_val[7]) + 0.2 * (avg_val[8])
        mem_avg = ( avg_val[9] - ( 0.5 * (avg_val[10]) + 0.3 * (avg_val[11]) + 0.2 * (avg_val[12]) ) ) / 1000000
        user_avg = avg_val[13]
        timestamp = int(avg_val[14])
        avg_data.append([load_avg,util_avg,bd_avg,mem_avg,user_avg,timestamp])

        i = i + steps

    zipped = list(zip(*avg_data))
    return zipped


path = home + "/eagle3_daytime/"
dirs = os.listdir(path)

# print(dirs)
c = 0
node_data = {}
for each in dirs:
    db = path + each + "/data.db"
    print("\n\n" + db)
    if os.path.isfile(db):
        try:
            data = read_node_data_from_db(db)
            node_data[int(each[5:])] = data
        except:
            pass

print(node_data)

plt.figure(0)
for key in sorted(node_data.keys()) :
    value = node_data[key]
    # print( "\n" +  str(key))
    if value == None or len(value) != 6:
        continue

    plt.plot(value[5], value[0], label="node" + str(key))
    
figure = plt.gcf() # get current figure
figure.set_size_inches(14, 10)

plt.legend()
plt.savefig('d1_load.jpg')

plt.figure(1)
for key in sorted(node_data.keys()) :
    value = node_data[key]
    # print( "\n" +  str(key))
    if value == None or len(value) != 6:
        continue

    plt.plot(value[5], value[1], label="node" + str(key))
    
figure = plt.gcf() # get current figure
figure.set_size_inches(14, 10)
plt.legend()
plt.savefig('d1_util.jpg')

plt.figure(2)
for key in sorted(node_data.keys()) :
    value = node_data[key]
    # print( "\n" +  str(key))
    if value == None or len(value) != 6:
        continue

    plt.plot(value[5], value[2], label="node" + str(key))
    
figure = plt.gcf() # get current figure
figure.set_size_inches(14, 10)
plt.legend()
plt.savefig('d1_bw.jpg')


plt.figure(3)
for key in sorted(node_data.keys()) :
    value = node_data[key]
    # print( "\n" +  str(key))
    if value == None or len(value) != 6:
        continue

    plt.plot(value[5], value[3], label="node" + str(key))
    
figure = plt.gcf() # get current figure
figure.set_size_inches(14, 10)
plt.legend()
plt.savefig('d1_memory.jpg')

plt.figure(4)
for key in sorted(node_data.keys()) :
    value = node_data[key]
    # print( "\n" +  str(key))
    if value == None or len(value) != 6:
        continue

    plt.plot(value[5], value[4], label="node" + str(key))
    
figure = plt.gcf() # get current figure
figure.set_size_inches(14, 10)
plt.legend()
plt.savefig('d1_user.jpg')
