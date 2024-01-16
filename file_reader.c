#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>


#define M 2150
#define N 1600
int* a[M];
static void file_converter() {

    FILE *file;
    file = fopen("trial.txt", "r");
    char str[10000];
    char* tok;
    for (int e =0; e < M; e++) {
        a[e] = (int*) malloc(N* sizeof(int));
    }
    int i = 0, j;
    while (1)
    {  
        if (fgets(str, 10000, file) != NULL) {
            
            //printf("%s", str);
            tok = strtok(str, ",");
            j = 0;
            a[i][j] = atoi(tok);
            //printf("%d\n", i);
            while (tok != NULL) {
                a[i][j] = atoi(tok);
                //printf("%3d", atoi(tok));
                tok = strtok(NULL, ",");
                j++;
                
            }
            i++;
        }
        else {
            break;
        }
    }
    /*for (int k = 0; k < M; k++) {
        printf("\n");
        for (int r = 0;r < N;r++) {
            printf("%3d", a[k][r]);
        }
    } */
}