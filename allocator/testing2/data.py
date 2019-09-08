from matplotlib import pyplot as plt
import numpy as np
import os
whole_data = {}
n=0
process =  [4,8,16,32]
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
            sum[0] = sum[0] + int(time_our) // 1000
            sum[1] = sum[1] + int(time_compute) // 1000
            sum[2] = sum[2] + int(time_random) // 1000
            sum[3] = sum[3] + int(time_sequence) // 1000
            # print(str(p) + "-" + str(s) + "-" + str(i) + " : " + str(time_our) + " " + str(time_compute) + " " + str(time_random) + " " + str(time_sequence) )

        print(str(p) + "-" + str(s) + " : " + str(sum[0]/4) + " " + str(sum[1]/4) + " " + str(sum[2]/4) + " " + str(sum[3]/4) )
        data[0] = data[0] + [sum[0]]
        data[1] = data[1] + [sum[1]]
        data[2] = data[2] + [sum[2]]
        data[3] = data[3] + [sum[3]]

    whole_data[p] = data

print(n)

print(whole_data)

for p in process:
    x = size
    plt.plot(x, whole_data[p][0], label='network and load aware')
    plt.plot(x, whole_data[p][1], label='laod aware')
    plt.plot(x, whole_data[p][2], label='random allocation')
    plt.plot(x, whole_data[p][3], label='sequence based')

    plt.xlabel('Data size')
    plt.ylabel('Time')

    plt.title("Time VS Data , Processes = " + str(p) + ", PPN = 4, Nodes = " + str(p//4))

    plt.legend()
    plt.savefig('process_count{0}.jpg'.format(p))
    plt.close()