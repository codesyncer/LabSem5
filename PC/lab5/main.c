#include <stdio.h>
#include <time.h>
#include <sys/time.h>
#include <omp.h>
#include <stdlib.h>
int main(void){
    struct timeval TimeValue_Start;
    struct timezone TimeZone_Start;
    struct timeval TimeValue_Final;
    struct timezone TimeZone_Final;
    long time_start, time_end;
    double time_overhead;
    const int N=100;
    int arr[N];
    srand(time(NULL));
    for(int i=0; i<N; ++i)
        arr[i] = rand();
    int i, minV = arr[0];
    omp_set_num_threads(4);
    gettimeofday(&TimeValue_Start, &TimeZone_Start);
    #pragma omp parallel for reduction(min : minV)
        for(i = 0; i< N; ++i)
            if(arr[i] < minV)
                minV = arr[i];
    gettimeofday(&TimeValue_Final, &TimeZone_Final);
    time_start = TimeValue_Start.tv_sec * 1000000 + TimeValue_Start.tv_usec;
    time_end = TimeValue_Final.tv_sec * 1000000 + TimeValue_Final.tv_usec;
    time_overhead = (time_end - time_start)/1000000.0;
    printf("\nMin: %d, Time in Seconds (T) : %lf\n",minV, time_overhead);
}