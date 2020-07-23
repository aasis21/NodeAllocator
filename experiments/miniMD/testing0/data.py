from matplotlib import pyplot as plt
import numpy as np
import os
whole_data = {}
n=0
for p in [4,8,16,32,64]:
    data = [[],[],[],[]]
    for s in [0,10,20,30,40,50]:
        sum = [0,0,0,0]
        for i in range(5):
            time_our = input()
            time_compute = input()
            time_random = input()
            time_sequence = input()
            n=n+4
            sum[0] = sum[0] + int(time_our)
            sum[1] = sum[1] + int(time_compute)
            sum[2] = sum[2] + int(time_random)
            sum[3] = sum[3] + int(time_sequence)
            # print(str(p) + "-" + str(s) + "-" + str(i) + " : " + str(time_our) + " " + str(time_compute) + " " + str(time_random) + " " + str(time_sequence) )

        print(str(p) + "-" + str(s) + " : " + str(sum[0]/4) + " " + str(sum[1]/4) + " " + str(sum[2]/4) + " " + str(sum[3]/4) )
        data[0] = data[0] + [sum[0]]
        data[1] = data[1] + [sum[1]]
        data[2] = data[2] + [sum[2]]
        data[3] = data[3] + [sum[3]]
    for each in data:
        each.insert(0, each.pop(0))
    whole_data[p] = data

print(n)

print(whole_data)

for p in [4,8,16,32,64]:
    x = [0, 10,20,30,40,50]
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