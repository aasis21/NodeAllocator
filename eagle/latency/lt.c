#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "mpi.h"

int main( int argc, char *argv[])
{
    int myrank, size, len;
    char name[MPI_MAX_PROCESSOR_NAME];


    MPI_Init(&argc, &argv);
    MPI_Comm_rank( MPI_COMM_WORLD, &myrank );
    MPI_Comm_size( MPI_COMM_WORLD, &size );
    MPI_Get_processor_name(name, &len);

    MPI_Status status;

    int msg_size = 64;
    char arr[msg_size];    
    int trips = 250;

    // loop over the shift i.e  senderRank = i, recieverRank = (i+shift)%30
    for(int shift=1;shift < size;shift++){
        int label[size];
        for(int i=0;i<size;i++){
            label[i] = 0;
        }
        int non_handled = size;

        // Each layer gives the pair that will do communication in parallel.
        // nodes that do not send or recieve will wait.
        // all layer is synced with mpi_barrier. Max 3 layer possible for any shift.
        while(non_handled>0){
            // for every shift and layer: if sender is selected , then its reciever can't be a sender in the given layer.
            for(int i=0;i< size;i++){
                if (label[i] == 0 && label[(i+shift)%size] !=1){
                    label[i] = 1;
                    if(label[(i+shift)%size] == -1){
                        label[(i+shift)%size] = 50;
                    }else{
                        label[(i+shift)%size] = 100;
                    }
                } 
            
            }
            // label array will contain information on which node will send, which will recv and which will be idle;

            // sync all process
            MPI_Barrier(MPI_COMM_WORLD);

            double s_time = MPI_Wtime();
            if(label[myrank] == 1){
                // will send data in this layer
                for(int i=0; i< trips; i++){
                    MPI_Send(arr, msg_size  , MPI_BYTE, (myrank + shift) % size, 99, MPI_COMM_WORLD);
                    MPI_Recv(arr, msg_size, MPI_BYTE, (myrank + shift) % size , 99 , MPI_COMM_WORLD, &status);
                }
            }else if(label[myrank] == 50 || label[myrank] == 100){
                // will recieve data in this layer
                for(int i=0; i< trips; i++){
                    MPI_Recv(arr, msg_size , MPI_BYTE, (myrank - shift + size) % size, 99, MPI_COMM_WORLD, &status);
                    MPI_Send(arr, msg_size  , MPI_BYTE, (myrank - shift + size) % size , 99, MPI_COMM_WORLD);
                }
            }            
            double time_taken = MPI_Wtime() - s_time;
            
            // Taking max time of sender and reciever for bw.
            if(label[myrank] == 1){
                MPI_Send(&len, 1 , MPI_INT, (myrank + shift) % size, 99, MPI_COMM_WORLD);
                MPI_Send(name, len , MPI_CHAR, (myrank + shift) % size, 99, MPI_COMM_WORLD);
                MPI_Send(&time_taken, 1 , MPI_DOUBLE, (myrank + shift) % size, 99, MPI_COMM_WORLD);
            }else if(label[myrank] == 50 || label[myrank] == 100){
                double sender_time_taken = 0;
                double max_time_taken = time_taken;
                int length;
                char other[MPI_MAX_PROCESSOR_NAME];
                MPI_Recv(&length, 1 , MPI_INT, (myrank - shift + size) % size, 99, MPI_COMM_WORLD, &status);
                MPI_Recv(other, length , MPI_CHAR, (myrank - shift + size) % size, 99, MPI_COMM_WORLD, &status);
                MPI_Recv(&sender_time_taken, 1 , MPI_DOUBLE, (myrank - shift + size) % size, 99, MPI_COMM_WORLD, &status);
                if(sender_time_taken > time_taken){
                    max_time_taken = sender_time_taken;
                }
                printf("%s %s %.2lf\n", other, name,  max_time_taken * 1000000 / trips );
            }

            // mark all handled source
            non_handled = 0;
            for(int i=0;i< size;i++){
                if(label[i]==0 || label[i]==100 ){
                    label[i] = 0;
                    non_handled++;
                }else{
                    label[i] = -1;
                }                
            }
            // sync all process at a layer of current shift value
            MPI_Barrier(MPI_COMM_WORLD);
        }
    }


    MPI_Finalize();
    return 0;
}
