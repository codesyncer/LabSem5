#include<stdio.h>
#include<omp.h>
#define SIZE 1000

void print_sums(int mat[SIZE][SIZE]){
#pragma omp for
    for(int i = 0; i < SIZE; ++i){
        int sum = 0;
        for(int j = 0; j < SIZE; ++j)
            sum += mat[i][j];
        // printf("Row %d: %d\n", i, sum);
    }
#pragma omp for
    for(int i = 0; i < SIZE; ++i){
        int sum = 0;
        for(int j = 0; j < SIZE; ++j)
            sum += mat[j][i];
        // printf("Col %d: %d\n", i, sum);
    }
}

int mat[SIZE][SIZE];
void main()
{
    for(int i = 0; i < SIZE; ++i)
        for(int j = 0; j < SIZE; ++j)
            mat[i][j] = SIZE*i+j;
    double t1, t2;
    t1 = omp_get_wtime();
    omp_set_num_threads(2);
#pragma omp parallel
{
    print_sums(mat);
}
    t2 = omp_get_wtime();
    printf("Time: %lf\n", t2-t1);
}