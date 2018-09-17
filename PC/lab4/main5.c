#include<stdio.h>
#include<omp.h>
#define SIZE 100000

float inc(float mat[2][SIZE]){
    float inc_amt, total_inc = 0;
#pragma omp for 
    for(int i = 0; i < SIZE; ++i){
        inc_amt = mat[1][i]*0.6;
        if (inc_amt <= 5000)
            total_inc += inc_amt;
        else
            total_inc += inc_amt - .2*(inc_amt - 5000);
    }
    return total_inc;
}

float db[2][SIZE];
int main(){
    double t1, t2;
    t1 = omp_get_wtime();
    omp_set_num_threads(2);
#pragma omp parallel
{
#pragma omp master nowait
    printf("%f\n", inc(db));
}
    t2 = omp_get_wtime();
    printf("Time: %lf\n", t2 - t1);
    return 0;
}
    