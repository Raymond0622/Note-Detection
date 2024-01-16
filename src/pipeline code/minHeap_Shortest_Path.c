#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <time.h>
#include <unistd.h>
//#include <sys/wait.h>
#include "minHeapInitialize.c"

#define STAFF_HEIGHT 11

int size;
int x1, x2, yy1, yy2;
int qq;
int* ret;
int* trimmed;

void sinkUp(int pos) {

    struct node v = vertex[spt[pos]];
    int k = (int) ceil((pos - 1)/((double) 2));
    struct node parent = vertex[spt[k]];
    //printf("%d", parent.pos);
    //getchar();
    while (v.dist < parent.dist && k >= 1) {
        spt[k] = v.value;
        spt[pos] = parent.value;
        vertex[spt[k]].pos = k;
        vertex[spt[pos]].pos = pos;

        pos = k;
        
        k = (int) ceil((pos - 1)/ ((double) 2));
        parent = vertex[spt[k]];
        //printf("%d Parent: %f %d, Child: %f %d\n", k, parent.dist, parent.pos, v.dist, v.pos);
        //getchar();
        
    }
}

void sinkDown(int pos) {

    int left = 2*pos;
    int right = 2*pos + 1;
    int which;
    
    if (spt[right] == -1) {
        if (spt[left] != -1) {
            struct node* v = &vertex[spt[pos]];
            struct node* parent = &vertex[spt[left]];
            if ((*v).dist > (*parent).dist) {
                spt[left] = (*v).value;
                spt[pos] = (*parent).value;

                (*v).pos = left;
                (*parent).pos = pos;
            }
        }
    }
    else {
        if (vertex[spt[left]].dist < vertex[spt[right]].dist) {
            which = left;
        }
        else {
            which = right;
        }
        struct node* v = &vertex[spt[pos]];
        struct node* parent = &vertex[spt[which]];

        while ((*v).dist > (*parent).dist) {
            
            spt[which] = (*v).value;
            spt[pos] = (*parent).value;

            (*v).pos = which;
            (*parent).pos = pos;

            pos = which;
            left = 2*which;
            right = 2*which + 1;

            if (spt[right] == -1) {
                if (spt[left] != -1) {
                    v = &vertex[spt[pos]];
                    parent = &vertex[spt[left]];
                    if ((*v).dist > (*parent).dist) {
                        spt[left] = (*v).value;
                        spt[pos] = (*parent).value;

                        (*v).pos = left;
                        (*parent).pos = pos;
                    }
                }
                break;
            }

            if (vertex[spt[left]].dist < vertex[spt[right]].dist) {
                which = left;
            }
            else {
                which = right;
            }
            parent = &vertex[spt[which]];
            
        }
    }
    
}
struct node getMin() {
    return vertex[spt[1]];
}
double dist(int p, int q) {
  
    yy1 = p / N;
    x1 = p % N;
    yy2 = q / N;
    x2 = q % N;

    return sqrt(pow((x1 -x2), 2) + pow((yy1 - yy2), 2));
}
double weight_determine(struct node v, struct node w) {
    double weight;
    if (v.color < 50 || w.color < 50) {
        weight = 2;
    }
    else {
        weight = 6;
    }
    if (dist(v.value, w.value) > 1) {
        weight = weight * 3;
    }
    return weight;

}
void update(struct node* v) {
    struct node* n = (*v).next;
    if (!((*v).visited)) {
        while (n != NULL) {
            //if (!(vertex[(*n).value]).visited) {
                double weight = weight_determine(*v, *n);
                if ((*v).dist + weight < vertex[(*n).value].dist) {
                    vertex[(*n).value].dist = weight + (*v).dist;
                    vertex[(*n).value].lastVisited = (*v).value;
                    sinkUp(vertex[(*n).value].pos);
                } 
            //}
            n = (*n).next;
        }
        qq++;
    }  
}

void show() {
    for (int i = 0; i < N*Q;i++) {
        printf("Distance to Vertex %d: %f\n", i, vertex[i].dist);
    }
}

void retrack(int I, FILE* out) {

    int pp = 0;
    int dd = 1599;
    while(dd != 0) {
        dd = vertex[dd].lastVisited;
        ret[pp] = dd + I*N;
        pp++;
        
    }
    int w, x, y;
    int QQ = 0;
    double black = 0, sumX = 0, sumY = 0, num = 0, denX = 0, denY = 0;
    int black_counter = 0;

    for (int i = 0;i < pp; i++) {
        w = ret[i];
        x = w % N;
        y = w / N;
        if (a[y][x] < 100) {
            black++;
            black_counter++;
            if (black_counter >= 2*STAFF_HEIGHT) {
                trimmed[QQ] = i;
                QQ++;
            }
        }
        else {
            black_counter = 0;
        }
    }
    int s = trimmed[0] - STAFF_HEIGHT, e = trimmed[QQ-1], K = 0;
    int* X = (int *) malloc(sizeof(int)*(e - s));
    int* Y = (int *) malloc(sizeof(int)*(e - s));
    int k = 0;
    if (black / pp > 0.75) {
        for (int t = s; t < e; t++) {
            X[K] = ret[t] % N;
            Y[K]= ret[t] / N;
            sumX = sumX + x;
            sumY = sumY + y;
            K++;
        }
        double meanX = sumX / (e - s);
        double meanY = sumY / (e - s);
        double diffX, diffY;
        for (int w = 0; w < (e - s); w++) {
            diffX = X[w] - sumX;
            diffY = Y[w] - sumY;
            num = num + diffX * diffY;
            denX = denX + diffX * diffX;
            denY = denY + diffY * diffY;
        }

        if (true) {
            for (int t =s; t <e; t++) {
                fprintf(out, "%d,", ret[t]);
            }
        }
    }    

}
void freeUp() {
    free(spt);
    free(vertex);
    free(ret);
    free(trimmed);
}
void what(int i) {
    printf("%d\n", i);
}

void run(int i, FILE* out) {
    ret = malloc(sizeof(int)*2*N);
    trimmed = malloc(sizeof(int)*2*N);
    init(i);
    qq = 0;
    struct node min = getMin();
    
    while (qq < N*Q) {
        spt[1] = spt[N*Q - qq];
        spt[N*Q - qq] = -1;

        sinkDown(1);
        update(&min);
        vertex[min.value].visited = true;
        
        min = getMin();
    
    }
    retrack(i, out);
    freeUp();
    //show();
}

int main() {
    file_converter();
    darken();
    FILE *out;
    out = fopen("out.txt", "w");

    for (int i = 0; i < M-Q;i = i + 4) {
        run(i, out);
    }

    // We can fork() to multiprocess each shortest path process. The code below is
    // a sample code of how one does so using 2 forks() which create 4 total
    // processes. 

    /*
    char name[] = "outX.txt";
    for (int i = 20; i < 24;i++) {
        name[3] = i + '0';
        files[i - 20] = fopen(name, "w");
    }

    int n1 = fork();
    int n2 = fork();

    if (n1 > 0 && n2 > 0) {
        for (int i = 0; i < M-Q;i = i + 16) {
            run(i, files[0]);
        }
        exit(0);
    }   
    else if (n1 == 0 && n2 > 0) {
        for (int i = 4; i < M-Q;i = i + 16) {
            run(i, files[1]);
        }
        exit(0);
    }  
    else if (n1 > 0 && n2 == 0) {
        for (int i = 8; i < M-Q;i = i + 16) {
            run(i, files[2]);
        }
        exit(0);
    }  
    else {
        for (int i = 12; i < M-Q;i = i + 16) {
            run(i, files[3]);
        }

    }  
    */

    // Print how long the process took

    //printf("Time: %f\n", ((double)(t))/CLOCKS_PER_SEC);
}
