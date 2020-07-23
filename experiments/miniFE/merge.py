from matplotlib import pyplot as plt
import numpy as np
import os
whole_data = {}
vwhole_data = {}

n=0
# process =  [8,16,32,48,64,80,96]
process = [32]
size = [ 24, 48, 96, 144 , 256, 384]


for p in process:
    data = [[],[],[],[],[]]
    vdata = [[],[],[],[],[]]
    for s in size:
        sum = [0,0,0,0,0]
        times = [[],[],[],[],[]]
        samp=4
        for i in range(samp):
            time_impr = 1000
            time_our = input() 
            time_compute = input()
            time_random = input()
            time_sequence = input()
            n=n+5
            sum[0] = sum[0] + int(time_impr) / 1000
            sum[1] = sum[1] + int(time_our) / 1000
            sum[2] = sum[2] + int(time_compute) / 1000
            sum[3] = sum[3] + int(time_random) / 1000
            sum[4] = sum[4] + int(time_sequence) / 1000
           

            times[0].append(int(time_impr)/1000)
            times[1].append(int(time_our)/1000)
            times[2].append(int(time_compute)/1000)
            times[3].append(int(time_random)/1000)
            times[4].append(int(time_sequence)/1000)

        variance = [round(np.std(li) / np.mean(li),3) for li in times]
        vdata = variance
        data[0] = data[0] + [sum[0]/samp]
        data[1] = data[1] + [sum[1]/samp]
        data[2] = data[2] + [sum[2]/samp]
        data[3] = data[3] + [sum[3]/samp]
        data[4] = data[4] + [sum[4]/samp]

    whole_data[p] = data
    vwhole_data[p] = vdata

for p in process:
  print("process :",p)
  for i in range(5):
    print(whole_data[p][i])

# print(vwhole_data)
vmat = np.array([vwhole_data[key] for key in  vwhole_data.keys() ])[:,:]
vari = vmat.mean(axis=0)
print("COV:",vari)



def find_avg_imp(base, idx):
    max_impr = 0
    min_impr = 100000000
    avg_impr = 0
    for p in process:
        data = whole_data[p]
        impr_sum = 0
        for i in range(sizesrt,sizeend):
            impr = ( data[idx][i] - data[base][i]) / data[idx][i]
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



sizesrt = 0
sizeend = 6  
# process = [64]
# process =  [96]

print("gain over load aware")
print(find_avg_imp(1,2))

print("gain over random")
print(find_avg_imp(1,3)) 

print("gain over sequential")
print(find_avg_imp(1,4))


for p in process:
    x = [e for e in size][1:]
    plt.plot(x, whole_data[p][3][1:], label='random', marker='.', color='red')
    plt.plot(x, whole_data[p][4][1:], label='sequential',  marker='.')
    plt.plot(x, whole_data[p][2][1:], label='load aware',  marker='.')
    plt.plot(x, whole_data[p][1][1:], label='network and load aware',  marker='.')
    
    

    plt.xlabel('Dimension')
    plt.ylabel('Time(seconds)')

    plt.title("Time vs size, Processes = " + str(p) + ", PPN = 4, Nodes = " + str(p//4))

    plt.legend()
    plt.savefig('minife_process_count{0}.jpg'.format(p))
    plt.close()
