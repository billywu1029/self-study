#include <stdio.h>

#define MAXN 300
#define FILENAME_MAX_SIZE 100
#define NUM_INPUTS 10

typedef struct Matrix {
    size_t R, C;
    int index[MAXN][MAXN];
} Matrix;

void read_matrix(FILE* fp, Matrix* X) {
    printf("Reading matrix from file...\n");
    fscanf(fp, "%zu %zu", &X->R, &X->C);

    for (int r = 0; r < X->R; r++) {
        for (int c = 0; c < X->C; c++) {
            fscanf(fp, "%d", &X->index[r][c]);
        }
    }
}

void write_matrix(FILE* fp, Matrix* X) {
    printf("Writing matrix to file...\n");
    // Assumes R, C, and index are non-null + valid matrix sizes/values
    fprintf(fp, "%zu %zu\n", X->R, X->C);

    for (int r = 0; r < X->R; r++) {
        for (int c = 0; c < X->C - 1; c++) {
            fprintf(fp, "%d ", X->index[r][c]);
        }
        fprintf(fp, "%d\n", X->index[r][X->C - 1]);
    }
}


int main() {
    for (int i = 1; i <= NUM_INPUTS; i++) {
        Matrix A, B, C;
        char infname[FILENAME_MAX_SIZE];
        char outfname[FILENAME_MAX_SIZE];
        sprintf(infname, "matrix.%d.in", i);
        sprintf(outfname, "matrix.%d.out", i);
        FILE *infile = fopen(infname, "r");
        FILE *outfile = fopen(outfname, "w");

        read_matrix(infile, &A);
        read_matrix(infile, &B);
        write_matrix(outfile, &A);
    }
}

