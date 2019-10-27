/******************************************************************************
* FILE: mpi_latency.c
* DESCRIPTION:  
*   MPI Latency Timing Program - C Version
*   In this example code, a MPI communication timing test is performed.
*   MPI task 0 will send "reps" number of k byte messages to MPI task 1,
*   waiting for a reply between each rep. Before and after timings are made 
*   for each rep and an average calculated when completed.
******************************************************************************/
#include "mpi.h"
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>
#define	NUMBER_REPS	250

int main (int argc, char *argv[])
{
   int numtasks, rank;  
   int reps = NUMBER_REPS;
   int message_size = 64;            
   char msg[message_size];                
   MPI_Status status; 

   MPI_Init(&argc,&argv);
   MPI_Comm_size(MPI_COMM_WORLD,&numtasks);
   MPI_Comm_rank(MPI_COMM_WORLD,&rank);
   if (rank == 0 && numtasks != 2) {
      printf("Number of tasks = %d\n",numtasks);
      printf("Only need 2 tasks - extra will be ignored...\n");
   }
   MPI_Barrier(MPI_COMM_WORLD);

   if (rank == 0) {
      /* round-trip latency timing test */
      // printf("task %d has started...\n", rank);
      // printf("Beginning latency timing test. Number of reps = %d.\n", reps);
      // printf("***************************************************\n");
      // printf("Rep#       T1               T2            deltaT\n");
      double T1,T2,sumT,deltaT, avgT, T3, T4;
      T3 = MPI_Wtime();
      for (int n = 1; n <= reps; n++) {
         
         T1 = MPI_Wtime();    
         int rc = MPI_Send(msg, message_size, MPI_BYTE, 1 , 99 , MPI_COMM_WORLD);
         if (rc != MPI_SUCCESS) {
            // printf("Send error in task 0!\n");
            MPI_Abort(MPI_COMM_WORLD, rc);
            exit(1);
         }
         rc = MPI_Recv(msg, message_size, MPI_BYTE, 1 , 99 , MPI_COMM_WORLD, &status);
         if (rc != MPI_SUCCESS) {
            // printf("Receive error in task 0!\n");
            MPI_Abort(MPI_COMM_WORLD, rc);
            exit(1);
         }
         T2 = MPI_Wtime(); 
         deltaT = T2 - T1;
         // printf("%4d  %8.8f  %8.8f  %2.8f\n", n, T1, T2, deltaT);
         sumT += deltaT;
      }
      T4 = MPI_Wtime(); 

      avgT = (sumT*1000000)/reps;
      printf("%d %d\n", (int)avgT, (int)( (T4-T3)*1000000)/reps  );
      // printf("*** Avg one way latency = %f microseconds\n", avgT/2);

   } else if (rank == 1) {
      // printf("task %d has started...\n", rank);
      for (int n = 1; n <= reps; n++) {
         int rc = MPI_Recv(msg, message_size, MPI_BYTE, 0 , 99, MPI_COMM_WORLD, &status);
         if (rc != MPI_SUCCESS) {
            // printf("Receive error in task 1!\n");
            MPI_Abort(MPI_COMM_WORLD, rc);
            exit(1);
         }
         rc = MPI_Send(msg, message_size, MPI_BYTE, 0, 99, MPI_COMM_WORLD);
         if (rc != MPI_SUCCESS) {
            // printf("Send error in task 1!\n");
            MPI_Abort(MPI_COMM_WORLD, rc);
            exit(1);
         }
      }
   }

   MPI_Finalize();
   exit(0);
}