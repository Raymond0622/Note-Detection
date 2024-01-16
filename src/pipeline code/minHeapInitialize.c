#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include "meh.c"
#include <time.h>
#include <unistd.h>

#define Q 23
#define STAFF_HEIGHT 11
struct node* vertex;
int* spt;

struct node {
    int value;
    int color;
    int pos;
    bool visited;
    double dist;
    int lastVisited;
    struct node* next;
};

void det(int* p, int* q, int k) {

    switch(k) {
        case 0:
            *q = *q - 1;
            break;
        case 1:
            *p = *p + 1;
            *q = *q - 1;
            break;
        case 2:
            *p = *p + 1;;
            break;
        case 3:
            *p = *p + 1;
            *q = *q + 1;
            break;
        case 4:
            *q = *q + 1;
            break;
        case 5:
            break;
    }
}
int sat(int* p, int* q) {
    if (*p < 0) {
        return 1;
    }
    if (*p >= N) {
        return 1;
    }
    if (*q < 0) {
        return 1;
    }
    if (*q >= M) {
        return 1;
    }
    return 0;
}

void darken() {
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < N;j++) {
            if (a[i][j] < 200) {
                a[i][j] = 0;
            }
            else {
                a[i][j] = 255;
            }
        }
    }
}

struct node* addList(struct node* first, struct node* new, int val, int color) {
    new->value = val;
    new->next = first;
    new->pos = val + 1;
    new->color = color;
    new->lastVisited = val;
    new->visited = false;
    return new;
}

void init(int start) {

    // vertex variable contains the heap nodes, with relevant information (i.e adjacent vertices, value (index value of graph), etc)
    // spt variable is the position of each heap node based on distance from (0, 0) vertex.
    // Initially, the first position (1) is going to be the 0, 0 node

    vertex = malloc(sizeof(struct node)* Q*N);
    spt = malloc(sizeof(int)*2*(Q*N + 1));

    for (int i =1; i < 2*(N*Q+1);i++) {
        if (i < N*Q +1) {
            spt[i] = i - 1;
        }
        else {
            spt[i] = -1;
        }
    }
    for (int i = 0; i < Q;i++) {
        for (int j = 0; j < N;j++) {
            struct node* first = NULL;
            for (int k = 0; k < 6; k++) {
                //p is y-axis, q is x-axis
                int p = i;
                int q = j;
                det(&q, &p, k);
                if (sat(&q, &p) == 0) {
                    struct node* new = malloc(sizeof(struct node));
                    new->dist = 1000000;
                    first = addList(first, new, N*p + q, a[p + start][q]);
                    //printf("%d\n", (*first).value);
                }
            }
            vertex[i*N + j] = *first;
        }
    }
    vertex[0].dist = 0;
}
/*int main() {
    file_converter();
    init();
    struct node v = vertex[0];
    while (v.next != NULL) {
        printf("%d\n", v.value);
        v = *(v.next);
    }
    printf("%d", v.value);
}*/
