import numpy as np
import os
from itertools import islice


# cat metadata.log | grep -F -e "load_1 :" -e "load_5 :" -e "load_15 :" -e "node :" > load.txt

process = [4, 8,16,32,64]
size = [8,16,24,32,40,48]

data = open("load.txt","r")

load_data = {}
for p in process:
    local_load_data={}
    for s in size:
        load_s = {}
        for i in range(5):
            load1 = data.readline().split(":")[1:]
            load15 = data.readline().split(":")[1:]
            load5 = data.readline().split(":")[1:]
            node = data.readline().split(":")[1:]
            load = {}
            for idx, n in enumerate(node):
                load[n.strip(" \n")] = ( float(load1[idx].strip(" \n")) + float(load5[idx].strip(" \n")) ) / 2
                # print(load)
            load_s[i] = load
        local_load_data[s] = load_s
    load_data[p] = local_load_data

data.close()

# data = open("users.txt","r")

# load_data = {}
# for p in process:
#     local_load_data={}
#     for s in size:
#         load_s = {}
#         for i in range(5):
#             node = data.readline().split(":")[1:]
#             load1 = data.readline().split(":")[1:]    
#             load = {}
#             for idx, n in enumerate(node):
#                 load[n.strip(" \n")] = float(load1[idx].strip(" \n")) 
#                 # print(load)
#             load_s[i] = load
#         local_load_data[s] = load_s
#     load_data[p] = local_load_data

# data.close()

data = open("allocation.txt","r")

allocation = {}
for p in process:
    p_alloc = {}
    for s in size:
        s_alloc = {}
        for i in range(5):
            alloc = {}
            num = p // 4
            alloc["our"] = [ d.strip(" \n").split("csews")[1].split(":")[0] for d in islice(data, num)]
            alloc["load"] = [ d.strip(" \n").split("csews")[1] for d in islice(data, num)]
            alloc["random"] = [ d.strip(" \n").split("csews")[1] for d in islice(data, num)]
            alloc["sequence"] = [ d.strip(" \n").split("csews")[1] for d in  islice(data, num)]
            s_alloc[i] = alloc
        p_alloc[s] = s_alloc
    allocation[p] = p_alloc

data.close()

process = [32]
size = [48]

load_avg = [[],[],[],[]]
for p in process:
    for s in size:
        for i in range(5):
            nds = allocation[p][s][i]["our"]
            lds = [load_data[p][s][i][k] for k in nds if k in load_data[p][s][i].keys()]
            our_l_avg = np.mean(lds)

            nds = allocation[p][s][i]["load"]
            lds = [load_data[p][s][i][k] for k in nds if k in load_data[p][s][i].keys()]
            load_l_avg = np.mean(lds)

            nds = allocation[p][s][i]["sequence"]
            lds = [load_data[p][s][i][k] for k in nds if k in load_data[p][s][i].keys()]

            sequence_l_avg = np.mean(lds)

            nds = allocation[p][s][i]["random"]
            lds = [load_data[p][s][i][k] for k in nds if k in load_data[p][s][i].keys()]
            random_l_avg = np.mean(lds)

            load_avg[0].append(our_l_avg)
            load_avg[1].append(load_l_avg)
            load_avg[2].append(sequence_l_avg)
            load_avg[3].append(random_l_avg)

print(np.mean(load_avg[0]), np.mean(load_avg[1]), np.mean(load_avg[2]), np.mean(load_avg[3]))