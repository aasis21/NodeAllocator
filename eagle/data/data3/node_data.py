import sys
import os,re
import time
from pathlib import Path
import sqlite3 
from statistics import mean 
from matplotlib import pyplot as plt
import pickle
import numpy as np



# try:
#     home = str(Path.home())
# except:
#     home = os.getenv("HOME")

# def read_node_data_from_db(db_file):
#     con = sqlite3.connect(db_file)
#     cur = con.cursor()
#     node_sql = """
#     SELECT * FROM node_monitor 

#     """
#     rows = []
#     try:
#         cur.execute(node_sql)
#         rows = cur.fetchall()
#     except:
#         print(" No data ")
#         return None

#     i = 0
#     steps = 1000
#     avg_data = []
#     while( i+steps < len(rows)):
#         # print("\n"+str(i) + ":" + str(i+steps))
#         slice = rows[i:i+steps]
#         zipped = zip(*slice)
#         avg_val = []
#         for each in list(zipped)[7:]:
#             avg_val.append( mean(each))
        
#         load_avg = ( 0.5 * (avg_val[0]) + 0.3 * (avg_val[1]) + 0.2 * (avg_val[2])) % 40
#         bd_avg = ( 0.5 * (avg_val[3]) + 0.3 * (avg_val[4]) + 0.2 * (avg_val[5]) ) / 1000000
#         util_avg = 0.5 * (avg_val[6]) + 0.3 * (avg_val[7]) + 0.2 * (avg_val[8])
#         mem_avg = ( avg_val[9] - ( 0.5 * (avg_val[10]) + 0.3 * (avg_val[11]) + 0.2 * (avg_val[12]) ) ) / 1000000000
#         user_avg = avg_val[13]
#         timestamp = int(avg_val[14])
#         avg_data.append([load_avg,util_avg,bd_avg,mem_avg,user_avg,timestamp])

#         i = i + steps

#     zipped = list(zip(*avg_data))
#     return zipped


# path = home + "/eagle/"
# dirs = os.listdir(path)

# # print(dirs)
# c = 0
# node_data = {}
# for each in dirs:
#     db = path + each + "/data.db"
#     print("\n\n" + db)
#     if os.path.isfile(db):
#         try:
#             data = read_node_data_from_db(db)
#             node_data[int(each[5:])] = data
#         except:
#             pass

# for key,val in node_data.items():
#     print(key)
#     if val == None or len(val) != 6:
#         continue
#     print(val[0])

# with open("data.pickle", 'wb') as db:
#     pickle.dump(node_data,db)

with open("data.pickle", "rb") as db:
    node_data = pickle.load(db)
del node_data[12]
all_stamp = []
all_load = []
all_util = []
all_bw = []
all_mem = []
for i in range(100):
    load = 0
    util = 0
    bw = 0
    mem = 0
    stamp = 0
    count = 0
    for key in sorted(node_data.keys()) :
        value = node_data[key]
        if value == None or len(value) != 6 or len(value[5]) < 100:
            continue
        value = node_data[key]
        load = load + value[0][i]
        util = util + value[1][i]
        bw = bw + value[2][i]
        mem = mem + value[3][i]
        stamp = stamp + value[5][i]
        count = count + 1
    all_stamp.append(stamp//count)
    all_load.append(load/count)
    all_util.append(util/count)
    all_bw.append(bw/count)
    all_mem.append(mem/count)    

print(node_data.keys())

node_data["all"] = [all_load, all_util, all_bw, all_mem, all_mem, all_stamp]

def plot_fig(node_data,keys, index, title, label , filename, y, x):
    plt.figure()
    
    for key in keys :
        value = node_data[key]
        if value == None or len(value) != 6 or len(value[5]) < 100:
            print("bro",len(value),len(value[5]))
            continue
        if key == "all":
            plt.plot(list(np.linspace(0,40,90)), value[index][0:90], label=label[key])
        else:
            plt.plot(list(np.linspace(0,40,90)), value[index][0:90], label=label[key])

    plt.legend()
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)
    plt.savefig(filename + '.jpg')

# keys = [ 25,"all", 12  ]
# label = {25: "Node A", 12 : "Node B" , "all" : "All nodes"}
k2 = 16
k1 = 25

keys = [ k1,"all", k2 ]
label = {k1: "Node A", k2 : "Node B" , "all" : "All nodes"}

# plot_fig(node_data, keys, 0, "CPU Load", label , "load", "Load" , "Time(hour)")
# plot_fig(node_data, keys, 1, "CPU Utilization", label,  "util", "% Utilization", "Time(hour)" )
# plot_fig(node_data, keys, 3, "Memory Usage", label,"mem", "Memory Usage(GB)", "Time(hour)")

def plot_two():
        
    fig, ax1 = plt.subplots()
    color = 'tab:green'
    ax1.set_xlabel('Time(hour)')
    ax1.set_ylabel('% Utilization')
    ax1.set(ylim=(0, 40))

    ax1.plot(list(np.linspace(0,40,90)), node_data["all"][1][0:90], label="Utilization", color=color)
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Memory Usage(GB)')  # we already handled the x-label with ax1
    ax2.set(ylim=(0, 10))

    ax2.plot(list(np.linspace(0,40,90)), node_data["all"][3][0:90], color=color, label="Memory Usage")
    ax2.tick_params(axis='y') #, labelcolor=color
    
    ax1.legend(loc=2)
    ax2.legend(loc= 1)
    # fig.tight_layout()  # otherwise the right y-label is slightly clipped

    plt.title("CPU Utilization and Memory Usage")
    plt.savefig("mem_util" + '.jpg')
    # plt.show()

plot_two()

# k2 = 4
# k1 = 1
keys = [ k1,"all", k2 ]
label = {k1: "Node A", k2 : "Node B" , "all" : "All nodes"}
plot_fig(node_data, keys, 2, "Node Network Usage", label, "bw", "Network Traffic(MBps)" , "Time(hour)")

# for key in sorted(node_data.keys()) :
#     value = node_data[key]
#     print( "\n" +  str(key))
#     if value == None or len(value) != 6:
#         continue
#     plt.figure()
#     plt.plot(value[5], value[0], label="node" + str(key))
#     plt.legend()
#     plt.title("Load")
#     plt.savefig( str(key) +  '_load.jpg')

#     plt.figure()
#     plt.plot(value[5], value[1], label="node" + str(key))
#     plt.legend()
#     plt.title("Util")
#     plt.savefig( str(key) +  '_util.jpg')

#     plt.figure()
#     plt.plot(value[5], value[2], label="node" + str(key))
#     plt.legend()
#     plt.title("Band")
#     plt.savefig( str(key) +  '_bandwidth.jpg')

#     plt.figure()
#     plt.plot(value[5], value[3], label="node" + str(key))
#     plt.legend()
#     plt.title("Mem")
#     plt.savefig( str(key) +  '_memory.jpg')

# plt.figure(0)
# for key in sorted(node_data.keys()) :
#     value = node_data[key]
#     print( "\n" +  str(key))
#     if value == None or len(value) != 6:
#         continue

#     plt.plot(value[5], value[0], label="node" + str(key))
    
# figure = plt.gcf() # get current figure
# figure.set_size_inches(14, 10)

# plt.legend()
# plt.savefig('d1_load.jpg')

# plt.figure(1)
# for key in sorted(node_data.keys()) :
#     value = node_data[key]
#     print( "\n" +  str(key))
#     if value == None or len(value) != 6:
#         continue

#     plt.plot(value[5], value[1], label="node" + str(key))
    
# figure = plt.gcf() # get current figure
# figure.set_size_inches(14, 10)
# plt.legend()
# plt.savefig('d1_util.jpg')

# plt.figure(2)
# for key in sorted(node_data.keys()) :
#     value = node_data[key]
#     print( "\n" +  str(key))
#     if value == None or len(value) != 6:
#         continue

#     plt.plot(value[5], value[2], label="node" + str(key))
    
# figure = plt.gcf() # get current figure
# figure.set_size_inches(14, 10)
# plt.legend()
# plt.savefig('d1_bw.jpg')


# plt.figure(3)
# for key in sorted(node_data.keys()) :
#     value = node_data[key]
#     print( "\n" +  str(key))
#     if value == None or len(value) != 6:
#         continue

#     plt.plot(value[5], value[3], label="node" + str(key))
    
# figure = plt.gcf() # get current figure
# figure.set_size_inches(14, 10)
# plt.legend()
# plt.savefig('d1_memory.jpg')

# plt.figure(4)
# for key in sorted(node_data.keys()) :
#     value = node_data[key]
#     print( "\n" +  str(key))
#     if value == None or len(value) != 6:
#         continue

#     plt.plot(value[5], value[4], label="node" + str(key))
    
# figure = plt.gcf() # get current figure
# figure.set_size_inches(14, 10)
# plt.legend()
# plt.savefig('d1_user.jpg')


