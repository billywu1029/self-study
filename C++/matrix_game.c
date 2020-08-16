#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <string.h>

typedef struct Matrix {
    int m, n;
    uint64_t rows;
    uint64_t cols;
} Matrix;

void clear_matrix(Matrix* A) {
    A->rows = 0;
    A->cols = 0;
}

void read_matrix(Matrix* A) {
    scanf("%d %d", &A->m, &A->n);
    for (int i = 0; i < A->m; i++) {
        for (int j = 0; j < A->n; j++) {
            int x;
            scanf("%d", &x);
            // Don't care if redundant assignment
            A->rows |= x << i;
            A->cols |= x << (A->n - j - 1);
        }
    }
}

void print_matrix(Matrix* A) {
    // Usage of PRIx64 formatting to print the uint64_t
    printf("Row marker bits: \n");
    printf("%" PRIx64 "\n", A->rows);
    printf("Column marker bits: \n");
    printf("%" PRIx64 "\n", A->cols);
}

char* game_winner(Matrix* A) {
    static char* name[2] = {"Ashish", "Vivek"};
    // Assuming Ashish always goes first
    int turn = 1; // 1 if Ashish's turn, 0 if Vivek's
    while (1) {
        int 
        // *************************************
            if (!A->rows[i]) {
                A->rows[i] = 1;
                found_row = 1;
                break;
            }
        // *************************************
        if (!found_row) {
            return name[turn];
        }
        
        int found_col = 0;
        for (int j = 0; j < A->n; j++) {
            // Find the first available row
            if (!A->cols[j]) {
                A->cols[j] = 1;
                found_col = 1;
                break;
            }
        }
        if (!found_col) {
            return name[turn];
        }
        turn ^= 1;
    }
}

int main() {
    int num_matrices;
    scanf("%d", &num_matrices);
    Matrix matrix;

    for (int i = 0; i < num_matrices; i++) {
        clear_matrix(&matrix);
        read_matrix(&matrix);
        print_matrix(&matrix);
        // char* answer = game_winner(&matrix);
        // printf("%s\n", answer);
    }
}
