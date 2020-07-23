from matplotlib import pyplot as plt
import numpy as np
import os
whole_data = {}
vwhole_data = {}

n=0
size = [ 144 ]
process = [4, 8,16,32,48,64,80]
gains = [[],[],[],[],[]]

for s in size:
    data = [[],[],[],[],[]]
    vdata = [[],[],[],[],[]]
    for p in process:
        sum = [0,0,0,0,0]
        samp=4
        for i in range(samp):
            time_impr = 1000
            time_our = int(input()) 
            time_compute = int(input())
            time_random = int(input())
            time_sequence = int(input())
            n=n+5
            sum[0] = sum[0] + int(time_impr) / 1000
            sum[1] = sum[1] + int(time_our) / 1000
            sum[2] = sum[2] + int(time_compute) / 1000
            sum[3] = sum[3] + int(time_random) / 1000
            sum[4] = sum[4] + int(time_sequence) / 1000
           
        data[0] = data[0] + [sum[0]/samp]
        data[1] = data[1] + [sum[1]/samp]
        data[2] = data[2] + [sum[2]/samp]
        data[3] = data[3] + [sum[3]/samp]
        data[4] = data[4] + [sum[4]/samp]

    whole_data[s] = data


for s in size:
  print("size :",s)
  for i in range(5):
    print(whole_data[s][i])

# def find_avg_imp(base, idx):
#     max_impr = 0
#     min_impr = 100000000
#     avg_impr = 0
#     for p in process:
#         data = whole_data[p]
#         impr_sum = 0
#         for i in range(sizesrt,sizeend):
#             impr = ( data[idx][i] - data[base][i]) / data[idx][i]
#             gains[idx].append(impr)
#             impr_sum = impr_sum + impr
#             if impr > max_impr:
#                 max_impr = impr
#             if impr < min_impr:
#                 min_impr = impr
#         avg_impr = avg_impr + impr_sum/(sizeend-sizesrt)
    
#     avg_impr = avg_impr / len(process)
#     print("Max Impv:" + str(max_impr*100))
#     print("Avg Impv:" + str( avg_impr*100))
#     print("Min Impv:" + str(min_impr*100))        
#     return str( round(avg_impr*100,1))


# def stats(i):
#     print("Mean: ", np.mean(gains[i]))
#     print("Median: ", np.median(gains[i]))
#     print("Max: ", np.max(gains[i]))


# sizesrt = 0
# sizeend = 6  

# print("gain over load aware")
# print(find_avg_imp(1,2))
# stats(2)


# print("gain over sequential")
# print(find_avg_imp(1,4))
# stats(4)

# print("gain over random")
# print(find_avg_imp(1,3)) 
# stats(3)


for s in size:
    x = [e for e in process][:]
    plt.plot(x, whole_data[s][3][:], label='random', marker='.', color='red')
    plt.plot(x, whole_data[s][4][:], label='sequential',  marker='.')
    plt.plot(x, whole_data[s][2][:], label='load aware',  marker='.')
    plt.plot(x, whole_data[s][1][:], label='network and load aware',  marker='.')
    
    

    plt.xlabel('Process')
    plt.ylabel('Time(seconds)')

    plt.title("Time vs Process, Size = " + str(s) + ", PPN = 4" )

    plt.legend()
    plt.savefig('fix_size_minife_size{0}.jpg'.format(s))
    plt.close()
