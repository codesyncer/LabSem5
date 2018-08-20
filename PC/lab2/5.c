#include<stdio.h>
#include<omp.h>
void main()
{
    double t1,t2;
    int arr[] = {1,2,3,4,5,6,7,8,9,10,11,12};
    int i, n= 12, sum= 0;    
    for(i=0; i<n; ++i)
        sum+= arr[i];
    printf("Sum: %d\n",sum);
    sum= 0;
    int nt = 4;
    int block = n%nt==0 ? n/nt: n/nt+1;
    t1=omp_get_wtime();
    #pragma omp parallel reduction(+:sum) num_threads(nt)
    {
        sum= 0;
        #pragma omp for 
            for(i=0;i<=block;++i){
                int n1= (i+1)*block;
                for(int j=n1-block; (j<n1 && j<n); ++j)
                    sum+= arr[j];
            }
    }
    t2=omp_get_wtime();
    printf("Time taken is %lf\n",t2-t1);
    printf("Sum: %d\n",sum);
}