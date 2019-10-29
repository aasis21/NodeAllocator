from matplotlib import pyplot as plt
import numpy as np
import os
whole_data = {}
n=0
process =  [4,8,16,32,64]
size = [8, 16, 24,32,40]
for p in process:
    data = [[],[],[],[],[]]
    for s in size:
        sum = [0,0,0,0,0]
        for i in range(5):
            time_imp = input()
            time_our = input() 
            time_compute = input()
            time_random = input()
            time_sequence = input()
            n=n+5
            sum[0] = sum[0] + int(time_imp) // 1000
            sum[1] = sum[1] + int(time_our) // 1000
            sum[2] = sum[2] + int(time_compute) // 1000
            sum[3] = sum[3] + int(time_random) // 1000
            sum[4] = sum[4] + int(time_sequence) // 1000
            # print(str(p) + "-" + str(s) + "-" + str(i) + " : " + str(time_our) + " " + str(time_compute) + " " + str(time_random) + " " + str(time_sequence) )

        print(str(p) + "-" + str(s) + " : " + str(sum[0]/5) + " " + str(sum[1]/5) + " " + str(sum[2]/5) + " " + str(sum[3]/5) + " " + str(sum[4]/5)  )
        data[0] = data[0] + [sum[0]/5]
        data[1] = data[1] + [sum[1]/5]
        data[2] = data[2] + [sum[2]/5]
        data[3] = data[3] + [sum[3]/5]
        data[4] = data[4] + [sum[4]/5]

    whole_data[p] = data

print(n)

print(whole_data)

for p in process:
    x = size
    plt.plot(x, whole_data[p][0], label='improved network and load aware')
    plt.plot(x, whole_data[p][1], label='network and load aware')
    plt.plot(x, whole_data[p][2], label='load aware')
    plt.plot(x, whole_data[p][3], label='random allocation')
    plt.plot(x, whole_data[p][4], label='sequence based')

    plt.xlabel('Data size')
    plt.ylabel('Time')

    plt.title("Time VS Data , Processes = " + str(p) + ", PPN = 4, Nodes = " + str(p//4))

    plt.legend()
    plt.savefig('process_count{0}.jpg'.format(p))
    plt.close()