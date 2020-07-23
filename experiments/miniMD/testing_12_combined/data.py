from matplotlib import pyplot as plt
import numpy as np
import os
whole_data = {}
vwhole_data = {}
gains = [[],[],[],[],[]]

n=0
process =  [4,8,16,32,64]
size = [8, 16, 24, 32, 40, 48]


for p in process:
    data = [[],[],[],[]]
    vdata = [[],[],[],[]]
    for s in size:
        sum = [0,0,0,0]
        times = [[],[],[],[]]
        for i in range(5):
            time_our = input() 
            time_compute = input()
            time_random = input()
            time_sequence = input()
            sum[0] = sum[0] + int(time_our) / 1000
            sum[1] = sum[1] + int(time_compute) / 1000
            sum[2] = sum[2] + int(time_random) / 1000
            sum[3] = sum[3] + int(time_sequence) / 1000

            times[0].append(int(time_our)/1000)
            times[1].append(int(time_compute)/1000)
            times[2].append(int(time_random)/1000)
            times[3].append(int(time_sequence)/1000)

        variance = [round(np.std(li) / np.mean(li),3) for li in times]
        vdata = variance
        data[0] = data[0] + [sum[0]/5]
        data[1] = data[1] + [sum[1]/5]
        data[2] = data[2] + [sum[2]/5]
        data[3] = data[3] + [sum[3]/5]

    whole_data[p] = data
    vwhole_data[p] = vdata

print(whole_data)
vmat = np.array([vwhole_data[key] for key in  vwhole_data.keys() ])[1:,:]
vari = vmat.mean(axis=0)
print(vmat,vari)

def find_avg_imp(base, idx):
    max_impr = 0
    min_impr = 100000000
    avg_impr = 0
    for p in process:
        data = whole_data[p]
        impr_sum = 0
        for i in range(sizesrt,sizeend):
            impr = ( data[idx][i] - data[base][i]) / data[idx][i]
            gains[idx].append(impr)
            impr_sum = impr_sum + impr
            if impr > max_impr:
                max_impr = impr
            if impr < min_impr:
                min_impr = impr
        avg_impr = avg_impr + impr_sum/(sizeend-sizesrt)
    
    avg_impr = avg_impr / len(process)
    print("Max Impv:" + str(max_impr*100))
    print("Avg Impv:" + str( avg_impr*100))
    print("Min Impv:" + str(min_impr*100))        
    return str( round(avg_impr*100,1))

# sizesrt = 0
# sizeend = 3
# size = [8, 16, 24 ]

# sizesrt = 3
# sizeend = 6
# size = [32, 40, 48]

# sizesrt = 0
# sizeend = 6
# size = [8, 16, 24, 32, 40, 48]




def stats(i):
    print("Mean: ", np.mean(gains[i]))
    print("Median: ", np.median(gains[i]))
    print("Max: ", np.max(gains[i]))


sizesrt = 0
sizeend = 6  

print("gain over load aware")
print(find_avg_imp(0,1))
stats(1)


print("gain over sequential")
print(find_avg_imp(0,3))
stats(3)

print("gain over random")
print(find_avg_imp(0,2)) 
stats(2)



for p in process:
    x = [e * e * e * 4 / 1000 for e in size]
    plt.plot(x, whole_data[p][2], label='random', marker='.', color='red')
    plt.plot(x, whole_data[p][3], label='sequential',  marker='.')
    plt.plot(x, whole_data[p][1], label='load aware',  marker='.')
    plt.plot(x, whole_data[p][0], label='network and load aware',  marker='.')
    
    

    plt.xlabel('Number of atoms(10^3 atoms)')
    plt.ylabel('Time(seconds)')

    plt.title("Time vs Atoms , Processes = " + str(p) + ", PPN = 4, Nodes = " + str(p//4))

    plt.legend()
    plt.savefig('process_count{0}.jpg'.format(p))
    plt.close()

# x = [4,8,16,32,64]
# s = 4 # i.e  prob size = 40
# for s in range(6):
#     pdata = []
#     for each in x:
#         pdata.append(whole_data[each][2][s])
#     plt.plot(x, pdata, label='random', marker='.')
#     pdata = []
#     for each in x:
#         pdata.append(whole_data[each][3][s])
#     plt.plot(x, pdata, label='sequential',  marker='.')

#     pdata = []
#     for each in x:
#         pdata.append(whole_data[each][1][s])
#     plt.plot(x, pdata, label='load aware',  marker='.')

#     pdata = []
#     for each in x:
#         pdata.append(whole_data[each][0][s])
#     plt.plot(x, pdata, label='network and load aware',  marker='.')

#     plt.xlabel('Number of Processes')
#     plt.ylabel('Time(seconds)')
#     plt.xticks(np.arange(0,72,8))
#     plt.title("Time vs Process Count , Number of atoms = " + str(size[s]*size[s]*size[s]*4) )

#     plt.legend()
#     plt.savefig("strong_scale" + str(s) + ".jpg")
#     plt.close()