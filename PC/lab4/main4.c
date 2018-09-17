#include<stdio.h>
#include<omp.h>
#define SIZE 1000

int T[SIZE][SIZE];
void mul(int m1[SIZE][SIZE], int r1, int c1, int m2[SIZE][SIZE], int r2, int c2, int m3[SIZE][SIZE]){
    if (c1 != r2) return;
// #pragma omp for collapse(2)
//     for(int i = 0; i < c2; ++i)
//         for(int j = 0; j < r2; ++j)
//             T[i][j] = m2[j][i];
#pragma omp for collapse(2)
    for(int i = 0; i < r1; ++i)
        for(int j = 0; j < c2; ++j)
        {
            int sum = 0;
            for(int k = 0; k < c1; ++k)
                // sum += m1[i][k]*T[i][k];
                sum += m1[i][k]*m2[k][j];
            m3[i][j] = sum;
        }
}

int m1[SIZE][SIZE], m2[SIZE][SIZE], m3[SIZE][SIZE];
void main(){
    double t1, t2;
    t1 = omp_get_wtime();
    omp_set_num_threads(2);
#pragma omp parallel
{
    mul(m1, SIZE, SIZE, m2, SIZE, SIZE, m3);
}
    t2 = omp_get_wtime();
    printf("Time: %lf\n", t2 - t1);
}
