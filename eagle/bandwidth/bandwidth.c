/****************************************************************************
* FILE: mpi_bandwidth.c
* DESCRIPTION:
*   Provides point-to-point communications timings for two mpi process.
****************************************************************************/ 
#include "mpi.h"
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>

#define MAXTASKS      8192
/* Change the next four parameters to suit your case */
#define STARTSIZE     100000
#define ENDSIZE       1000000
#define INCREMENT     200000
#define ROUNDTRIPS    100 

int main (int argc, char *argv[])
{
    MPI_Status status;
    int numtasks, rank, rc;
    MPI_Init(&argc,&argv);
    MPI_Comm_size(MPI_COMM_WORLD, &numtasks);
    if (numtasks != 2) {
        MPI_Abort(MPI_COMM_WORLD, rc);
        exit(0);
    }
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    int start = STARTSIZE;
    int end = ENDSIZE;
    int incr = INCREMENT;
    int rndtrps = ROUNDTRIPS;
    int tag = 99;
    char msgbuf[end];
    for (int i=0; i<end; i++)
        msgbuf[i] = 'x';

    MPI_Barrier(MPI_COMM_WORLD);

    if (rank == 0 ) {
        double resolution = MPI_Wtick();
        double totalall,avgall;
        int count = 0;
        for (int n=start; n<=end; n=n+incr) {
            double bw, bestbw, avgbw, worstbw, totalbw, t1, t2, thistime;
            bestbw = 0.0;
            worstbw = .99E+99;
            totalbw = 0.0;
            int nbytes =  sizeof(char) * n;
            for (int i=1; i<=rndtrps; i++){
                t1 = MPI_Wtime();
                MPI_Send(&msgbuf, n, MPI_CHAR, 1, tag, MPI_COMM_WORLD);
                MPI_Recv(&msgbuf, n, MPI_CHAR, 1, tag, MPI_COMM_WORLD, &status);
                t2 = MPI_Wtime();

                thistime = t2 - t1;
                bw = ((double)nbytes * 2) / thistime;
                totalbw = totalbw + bw;
            
                if (bw > bestbw ) bestbw = bw;
                if (bw < worstbw ) worstbw = bw;
            
            }

            bestbw = bestbw/1000000.0;
            avgbw = (totalbw/1000000.0)/(double)rndtrps;
            worstbw = worstbw/1000000.0;
            totalall = totalall + avgbw;
            count++;
            // printf("***Message size: %8d *** best  /  avg  / worst (MB/sec)\n",n);
            // printf("   OVERALL AVERAGES:          %4.2f / %4.2f / %4.2f \n\n", bestbw, avgbw, worstbw);
        }
        avgall = totalall/ count;
        // printf("    FINAL  OVERALL AVERAGES:          %4.2f / \n\n", avgall);
        printf("%d\n", (int)avgall);

    } else if (rank == 1) {
        for (int n=start; n<=end; n=n+incr) {
            for (int i=1; i<=rndtrps; i++){
                MPI_Recv(&msgbuf, n, MPI_CHAR, 0, tag, MPI_COMM_WORLD, &status);
                MPI_Send(&msgbuf, n, MPI_CHAR, 0, tag, MPI_COMM_WORLD);
            }
        }
    }


    MPI_Finalize();

}  /* end of main */
