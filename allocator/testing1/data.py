from matplotlib import pyplot as plt
import numpy as np
import os
whole_data = {}
n=0
process =  [8,16,32,64]
size = [8, 16, 24, 32, 40, 48]
for p in process:
    data = [[],[],[],[]]
    for s in size:
        sum = [0,0,0,0]
        for i in range(5):
            time_our = input() 
            time_compute = input()
            time_random = input()
            time_sequence = input()
            n=n+4
            sum[0] = sum[0] + int(time_our) / 1000
            sum[1] = sum[1] + int(time_compute) / 1000
            sum[2] = sum[2] + int(time_random) / 1000
            sum[3] = sum[3] + int(time_sequence) / 1000

        data[0] = data[0] + [sum[0]/5]
        data[1] = data[1] + [sum[1]/5]
        data[2] = data[2] + [sum[2]/5]
        data[3] = data[3] + [sum[3]/5]

    whole_data[p] = data

print(n)

print(whole_data)

def find_avg_imp(base, idx):
    max_impr = 0
    min_impr = 100000000
    avg_impr = 0
    for p in process:
        data = whole_data[p]
        impr_sum = 0
        for i in range(6):
            impr = ( data[idx][i] - data[base][i]) / data[idx][i]
            impr_sum = impr_sum + impr
            if impr > max_impr:
                max_impr = impr
            if impr < min_impr:
                min_impr = impr
        avg_impr = avg_impr + impr_sum/6
    
    avg_impr = avg_impr / len(process)
    print("Max Impv:" + str(max_impr*100))
    print("Avg Impv:" + str( avg_impr*100))
    print("Min Impv:" + str(min_impr*100))        

print("\nNetwork/load over Sequentail")
find_avg_imp(0,3)
print("\nNetwork/load over Random")
find_avg_imp(0,2)
print("\nNetwork/load over Load")
find_avg_imp(0,1)

print("\n Load over Sequential")
find_avg_imp(1,3)

print("\n Load over Random")
find_avg_imp(1,2)

print("\n Sequence over Random")
find_avg_imp(3,2)

for p in process:
    x = [e * e * e * 4 / 1000 for e in size]
    plt.plot(x, whole_data[p][2], label='random', marker='.')
    plt.plot(x, whole_data[p][3], label='sequential',  marker='.')
    plt.plot(x, whole_data[p][1], label='load aware',  marker='.')
    plt.plot(x, whole_data[p][0], label='network and load aware',  marker='.')
    
    

    plt.xlabel('Number of atoms(10^3 atoms)')
    plt.ylabel('Time(seconds)')

    plt.title("Time vs Atoms , Processes = " + str(p) + ", PPN = 4, Nodes = " + str(p//4))

    plt.legend()
    plt.savefig('process_count{0}.jpg'.format(p))
    plt.close()

x = [8,16,32,64]
s = 4 # i.e  prob size = 40
pdata = []
for each in x:
    pdata.append(whole_data[each][2][s])
plt.plot(x, pdata, label='random', marker='.')
pdata = []
for each in x:
    pdata.append(whole_data[each][3][s])
plt.plot(x, pdata, label='sequential',  marker='.')

pdata = []
for each in x:
    pdata.append(whole_data[each][1][s])
plt.plot(x, pdata, label='load aware',  marker='.')

pdata = []
for each in x:
    pdata.append(whole_data[each][0][s])
plt.plot(x, pdata, label='network and load aware',  marker='.')

plt.xlabel('Number of Processes')
plt.ylabel('Time(seconds)')
plt.xticks(np.arange(0,72,8))
plt.title("Time vs Process Count , Number of atoms = " + str(size[s]*size[s]*size[s]*4) )

plt.legend()
plt.savefig("strong_scale" + str(s) + ".jpg")
plt.close()
